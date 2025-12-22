#!/bin/bash
set -o pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
BASE_DIR="$SCRIPT_DIR/benchmarks"
LOG_DIR_NAME="logs"

# ================== CLI params (provided by user) ==================
# --model and --api_url are required flags (value may be empty string).
MODEL_NAME=""
API_URL=""
API_KEY=""
TEMPERATURE=""
TOP_P=""
PRESENCE_PENALTY=""
MAX_TOKENS=""
TIMEOUT=""
NUM_WORKERS=""
N=""

JUDGE_API_URL=""
JUDGE_MODEL=""
JUDGE_API_KEY=""

# Same switches as run_benchmarks.sh, but provided via CLI here.
ROLL_LABELED="FALSE"
USE_VL_MODE="FALSE"

# ================== Task list (execution order) ==================
TASK_NAMES=(
  "LAB-Bench"
  "GPQA" "AIME24" "AIME25" "LIVE_MATH_BENCH"
  "ChemBench" "Physics"
  "Qiskit_HumanEval" "MaScQA" "MSQA_Long" "MSQA_Short" "SciBench" "ProteinLMbench" "TOMG-Bench" "AMC23"
)

# ================== Task configs ==================
# Format: "DisplayName|BenchmarkDir|FixedArgs"
# - FixedArgs only contains task-specific args (NOT full params).
TASK_CONFIGS=(
  "ChemBench|ChemBench|"
  "GPQA|GPQA|"
  "LAB-Bench|LAB-Bench|"
  "MaScQA|MaScQA|"
  "MSQA_Long|MSQA_Long|"
  "MSQA_Short|MSQA_Short|"
  "Physics|Physics|"
  "Qiskit_HumanEval|Qiskit_HumanEval|"
  "ProteinLMbench|ProteinLMBench|"
  "SciBench|SciBench|"
  "TOMG-Bench|TOMG-Bench|"
  "AIME25|MATH|--task aime25"
  "AIME24|MATH|--task aime24"
  "AMC23|MATH|--task amc23"
  "LIVE_MATH_BENCH|MATH|--task live_math_bench"
)

show_help() {
  echo "Usage:"
  echo "  $0 --model <model_name> --api_url <api_url> [options] [task_number ...]"
  echo
  echo "Run benchmark tasks sequentially (by task number)."
  echo "If no task number is given, run all tasks."
  echo
  echo "Required options:"
  echo "  --model            Model name (required flag; value may be empty string \"\")"
  echo "  --api_url          API base url (required flag; value may be empty string \"\")"
  echo
  echo "Optional options (only included if provided):"
  echo "  --api_key"
  echo "  --temperature"
  echo "  --top_p"
  echo "  --presence_penalty"
  echo "  --max_tokens"
  echo "  --timeout"
  echo "  --num_workers"
  echo "  --n"
  echo "  --judge_api_url"
  echo "  --judge_model"
  echo "  --judge_api_key"
  echo "  --roll_labeled TRUE|FALSE"
  echo "  --use_vl_mode TRUE|FALSE"
  echo "  -h, --help"
  echo
  echo "Examples:"
  echo "  Run all:   $0 --model \"my_model\" --api_url \"http://127.0.0.1:8000/v1\" --api_key \"...\""
  echo "  Run 1&3:   $0 --model \"my_model\" --api_url \"http://127.0.0.1:8000/v1\" 1 3"
  echo "  With roll: $0 --model \"my_model\" --api_url \"...\" --roll_labeled TRUE 6"
  echo
  echo "Available tasks:"
  for i in "${!TASK_NAMES[@]}"; do
    echo "  $((i+1)). ${TASK_NAMES[i]}"
  done
}

_upper_bool() {
  local v="${1:-}"
  v="${v^^}"
  if [[ "$v" != "TRUE" && "$v" != "FALSE" ]]; then
    echo "Error: boolean must be TRUE or FALSE - $1" >&2
    exit 1
  fi
  echo "$v"
}

_mask() {
  local s="$1"
  [[ -z "$s" ]] && { echo ""; return; }
  local n=${#s}
  ((n<=6)) && { echo "***"; return; }
  echo "${s:0:4}***${s: -2}"
}

parse_args() {
  local model_provided=0
  local api_url_provided=0
  TASK_NUMS=()

  while [[ $# -gt 0 ]]; do
    case "$1" in
      -h|--help)
        show_help
        exit 0
        ;;
      --model)
        MODEL_NAME="${2-}"
        model_provided=1
        shift 2
        ;;
      --api_url)
        API_URL="${2-}"
        api_url_provided=1
        shift 2
        ;;
      --api_key) API_KEY="${2-}"; shift 2 ;;
      --temperature) TEMPERATURE="${2-}"; shift 2 ;;
      --top_p) TOP_P="${2-}"; shift 2 ;;
      --presence_penalty) PRESENCE_PENALTY="${2-}"; shift 2 ;;
      --max_tokens) MAX_TOKENS="${2-}"; shift 2 ;;
      --timeout) TIMEOUT="${2-}"; shift 2 ;;
      --num_workers) NUM_WORKERS="${2-}"; shift 2 ;;
      --n) N="${2-}"; shift 2 ;;
      --judge_api_url) JUDGE_API_URL="${2-}"; shift 2 ;;
      --judge_model) JUDGE_MODEL="${2-}"; shift 2 ;;
      --judge_api_key) JUDGE_API_KEY="${2-}"; shift 2 ;;
      --roll_labeled) ROLL_LABELED="$(_upper_bool "${2-}")"; shift 2 ;;
      --use_vl_mode) USE_VL_MODE="$(_upper_bool "${2-}")"; shift 2 ;;
      --)
        shift
        break
        ;;
      *)
        # Task numbers are positional (e.g. "1 3 5").
        if [[ "$1" =~ ^[0-9]+$ ]]; then
          TASK_NUMS+=("$1")
          shift
        else
          echo "Error: unknown option/argument: $1" >&2
          show_help
          exit 1
        fi
        ;;
    esac
  done

  # Remaining args after '--' are also task numbers.
  for x in "$@"; do
    if ! [[ "$x" =~ ^[0-9]+$ ]]; then
      echo "Error: task number must be numeric - $x" >&2
      exit 1
    fi
    TASK_NUMS+=("$x")
  done

  if [[ $model_provided -eq 0 || $api_url_provided -eq 0 ]]; then
    echo "Error: --model and --api_url are required flags (value may be empty string)" >&2
    show_help
    exit 1
  fi
}

parse_args "$@"

SELECTED_TASK_ORIGINAL_INDEXES=()
if [[ ${#TASK_NUMS[@]} -eq 0 ]]; then
  for i in "${!TASK_NAMES[@]}"; do
    SELECTED_TASK_ORIGINAL_INDEXES+=("$i")
  done
else
  for task_num in "${TASK_NUMS[@]}"; do
    original_index=$((task_num - 1))
    if (( original_index < 0 || original_index >= ${#TASK_NAMES[@]} )); then
      echo "Error: invalid task number - $task_num (valid range: 1..${#TASK_NAMES[@]})" >&2
      exit 1
    fi
    SELECTED_TASK_ORIGINAL_INDEXES+=("$original_index")
  done
fi

SELECTED_TASK_CONFIG_INDEXES=()
for original_index in "${SELECTED_TASK_ORIGINAL_INDEXES[@]}"; do
  task_name="${TASK_NAMES[original_index]}"
  found=0
  for config_index in "${!TASK_CONFIGS[@]}"; do
    config_name="$(echo "${TASK_CONFIGS[config_index]}" | cut -d'|' -f1)"
    if [[ "$config_name" == "$task_name" ]]; then
      SELECTED_TASK_CONFIG_INDEXES+=("$config_index")
      found=1
      break
    fi
  done
  if [[ $found -eq 0 ]]; then
    echo "Warning: task '${task_name}' (#$((original_index+1))) not found in TASK_CONFIGS, will skip" >&2
    SELECTED_TASK_CONFIG_INDEXES+=("")
  fi
done

TIMESTAMP="$(date +"%Y%m%d%H%M")"
START_TIME="$(date +"%Y-%m-%d %H:%M:%S")"
COMPLETED_TASKS=()
FAILED_TASKS=()

echo "===== Start sequential run: $START_TIME ====="
echo "Model: $MODEL_NAME"
echo "Timestamp: $TIMESTAMP"
echo "ROLL_LABELED: $ROLL_LABELED"
echo "USE_VL_MODE: $USE_VL_MODE"
echo "API_URL: $API_URL"
echo "API_KEY: $([[ -n "$API_KEY" ]] && echo "$(_mask "$API_KEY")" || echo "(not set)")"
echo
echo "Tasks to run:"
for original_index in "${SELECTED_TASK_ORIGINAL_INDEXES[@]}"; do
  task_num=$((original_index + 1))
  task_name="${TASK_NAMES[original_index]}"
  echo "  $task_num. $task_name"
done
echo "----------------------------------------"

build_common_args() {
  COMMON_ARGS=()
  [[ -n "$API_KEY" ]] && COMMON_ARGS+=(--api_key "$API_KEY")
  [[ -n "$TEMPERATURE" ]] && COMMON_ARGS+=(--temperature "$TEMPERATURE")
  [[ -n "$TOP_P" ]] && COMMON_ARGS+=(--top_p "$TOP_P")
  [[ -n "$PRESENCE_PENALTY" ]] && COMMON_ARGS+=(--presence_penalty "$PRESENCE_PENALTY")
  [[ -n "$MAX_TOKENS" ]] && COMMON_ARGS+=(--max_tokens "$MAX_TOKENS")
  [[ -n "$TIMEOUT" ]] && COMMON_ARGS+=(--timeout "$TIMEOUT")
  [[ -n "$NUM_WORKERS" ]] && COMMON_ARGS+=(--num_workers "$NUM_WORKERS")
  [[ -n "$N" ]] && COMMON_ARGS+=(--n "$N")

  [[ -n "$JUDGE_API_URL" ]] && COMMON_ARGS+=(--judge_api_url "$JUDGE_API_URL")
  [[ -n "$JUDGE_MODEL" ]] && COMMON_ARGS+=(--judge_model "$JUDGE_MODEL")
  [[ -n "$JUDGE_API_KEY" ]] && COMMON_ARGS+=(--judge_api_key "$JUDGE_API_KEY")
}

build_common_args

run_task() {
  local task_index="$1"
  local original_index="$2"
  local display_num=$((original_index + 1))
  local config="${TASK_CONFIGS[task_index]}"

  # Parse config
  local name rel_dir fixed_args
  IFS='|' read -r name rel_dir fixed_args <<< "$config"

  local start_time
  start_time="$(date +"%Y-%m-%d %H:%M:%S")"

  local task_dir="${BASE_DIR}/${rel_dir}"
  local model_name_no_spaces="${MODEL_NAME// /}"
  local log_file_name="${name}_${model_name_no_spaces}_${TIMESTAMP}.log"

  echo "----- Start task $display_num: $name ($start_time) -----"
  echo "Task dir: $task_dir"

  if [[ ! -d "$task_dir" ]]; then
    echo "Warning: directory not found, skip - $task_dir"
    FAILED_TASKS+=("$display_num:$name:dir_not_found")
    return 1
  fi

  pushd "$task_dir" &>/dev/null || {
    echo "Warning: unable to cd, skip - $task_dir"
    FAILED_TASKS+=("$display_num:$name:cd_failed")
    return 1
  }

  mkdir -p "$LOG_DIR_NAME" || {
    echo "Warning: unable to create log dir '$LOG_DIR_NAME', skip"
    FAILED_TASKS+=("$display_num:$name:mkdir_failed")
    popd &>/dev/null
    return 1
  }

  local log_path="${LOG_DIR_NAME}/${log_file_name}"
  local cmd=()
  cmd+=(python -u run.py)
  cmd+=(--model "$MODEL_NAME")
  cmd+=(--api_url "$API_URL")
  cmd+=("${COMMON_ARGS[@]}")

  # Model-specific tweaks
  if [[ "$MODEL_NAME" == "gpt-4" ]]; then
    cmd+=(--single_turn)
  fi

  if [[ "$ROLL_LABELED" == "TRUE" ]]; then
    cmd+=(--pass_data_path "/data02/home/zdhs0075/benchmark_suite/Rolldata1015/test_outputs_good/${rel_dir}.json")
  fi
  if [[ "$USE_VL_MODE" == "TRUE" ]]; then
    cmd+=(--use_vl_mode)
  fi

  if [[ -n "$fixed_args" ]]; then
    local fixed_arr=()
    # fixed_args is a simple space-separated string, e.g. "--task aime24"
    read -r -a fixed_arr <<< "$fixed_args"
    cmd+=("${fixed_arr[@]}")
  fi

  # Print command with masked secrets
  local cmd_print="${cmd[*]}"
  [[ -n "$API_KEY" ]] && cmd_print="${cmd_print//--api_key $API_KEY/--api_key ***}"
  [[ -n "$JUDGE_API_KEY" ]] && cmd_print="${cmd_print//--judge_api_key $JUDGE_API_KEY/--judge_api_key ***}"
  echo "Command: ${cmd_print}"
  echo "Log: $log_path"

  "${cmd[@]}" > "$log_path" 2>&1
  local exit_code=$?

  local end_time
  end_time="$(date +"%Y-%m-%d %H:%M:%S")"

  if [[ $exit_code -eq 0 ]]; then
    echo "Task $display_num: $name succeeded [$end_time]"
    COMPLETED_TASKS+=("$display_num:$name")
  else
    echo "Task $display_num: $name failed (exit=$exit_code) [$end_time]"
    FAILED_TASKS+=("$display_num:$name:exit=$exit_code")
  fi

  popd &>/dev/null
  return $exit_code
}

for i in "${!SELECTED_TASK_ORIGINAL_INDEXES[@]}"; do
  original_index="${SELECTED_TASK_ORIGINAL_INDEXES[i]}"
  task_index="${SELECTED_TASK_CONFIG_INDEXES[i]}"
  if [[ -z "${task_index}" ]]; then
    continue
  fi
  run_task "$task_index" "$original_index"
  echo "-------------------------------------"
done

echo "===== End sequential run: $(date +"%Y-%m-%d %H:%M:%S") ====="

