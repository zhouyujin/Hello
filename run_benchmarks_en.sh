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

# ================== Task list (available benchmark names) ==================
# Names are what the user types after --benchmarks (case-insensitive).
TASK_NAMES=(
  "chembench"
  "gpqa"
  "lab_bench"
  "mascqa"
  "msqa_long"
  "msqa_short"
  "physics"
  "qiskit_humaneval"
  "protein_lmbench"
  "scibench"
  "tomg_bench"
  "aime24"
  "aime25"
  "amc23"
  "live_math_bench"
)

# ================== Task configs ==================
# Format: "task_name|BenchmarkDir|FixedArgs"
# - FixedArgs only contains task-specific args (NOT full params).
TASK_CONFIGS=(
  "chembench|ChemBench|"
  "gpqa|GPQA|"
  "lab_bench|LAB-Bench|"
  "mascqa|MaScQA|"
  "msqa_long|MSQA_Long|"
  "msqa_short|MSQA_Short|"
  "physics|Physics|"
  "qiskit_humaneval|Qiskit_HumanEval|"
  "protein_lmbench|ProteinLMBench|"
  "scibench|SciBench|"
  "tomg_bench|TOMG-Bench|"
  "aime24|MATH|--task aime24"
  "aime25|MATH|--task aime25"
  "amc23|MATH|--task amc23"
  "live_math_bench|MATH|--task live_math_bench"
)

show_help() {
  echo "Usage:"
  echo "  $0 --model <model_name> --api_url <api_url> [options] [--benchmarks task1 task2 ...]"
  echo
  echo "Run benchmark tasks sequentially."
  echo "If --benchmarks is not provided, run all tasks."
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
  echo "  --benchmarks       Task names to run (space-separated)."
  echo "  -h, --help"
  echo
  echo "Examples:"
  echo "  Run all: $0 --model \"your-model\" --api_url \"your-api-url\" --api_key \"your-api-key\" --num_workers 10"
  echo "  Run some:"
  echo "    $0 --model \"your-model\" --api_url \"your-api-url\" --api_key \"your-api-key\" --num_workers 10 \\"
  echo "      --benchmarks scibench gpqa chembench"
  echo "  With roll:"
  echo "    $0 --model \"your-model\" --api_url \"...\" --roll_labeled TRUE --benchmarks scibench"
  echo
  echo "Available tasks:"
  for t in "${TASK_NAMES[@]}"; do echo "  - $t"; done
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
  BENCHMARKS=()
  local in_benchmarks=0

  while [[ $# -gt 0 ]]; do
    if [[ $in_benchmarks -eq 1 ]]; then
      if [[ "$1" == --* ]]; then
        in_benchmarks=0
      else
        BENCHMARKS+=("$1")
        shift
        continue
      fi
    fi
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
      --benchmarks) in_benchmarks=1; shift ;;
      --)
        shift
        break
        ;;
      *)
        echo "Error: unknown option/argument: $1" >&2
        show_help
        exit 1
        ;;
    esac
  done

  # Remaining args after '--' are treated as benchmarks too.
  for x in "$@"; do BENCHMARKS+=("$x"); done

  if [[ $model_provided -eq 0 || $api_url_provided -eq 0 ]]; then
    echo "Error: --model and --api_url are required flags (value may be empty string)" >&2
    show_help
    exit 1
  fi
}

parse_args "$@"

task_exists() {
  local want="${1,,}"
  for t in "${TASK_NAMES[@]}"; do
    if [[ "$t" == "$want" ]]; then
      return 0
    fi
  done
  return 1
}

get_config_index_by_task() {
  local want="${1,,}"
  for config_index in "${!TASK_CONFIGS[@]}"; do
    local config_name
    config_name="$(echo "${TASK_CONFIGS[config_index]}" | cut -d'|' -f1)"
    if [[ "$config_name" == "$want" ]]; then
      echo "$config_index"
      return 0
    fi
  done
  return 1
}

SELECTED_TASK_CONFIG_INDEXES=()
if [[ ${#BENCHMARKS[@]} -eq 0 ]]; then
  # Run all, in TASK_NAMES order.
  for t in "${TASK_NAMES[@]}"; do
    idx="$(get_config_index_by_task "$t")" || idx=""
    if [[ -z "$idx" ]]; then
      echo "Warning: task '$t' not found in TASK_CONFIGS, will skip" >&2
      continue
    fi
    SELECTED_TASK_CONFIG_INDEXES+=("$idx")
  done
else
  for t in "${BENCHMARKS[@]}"; do
    t_lc="${t,,}"
    if ! task_exists "$t_lc"; then
      echo "Error: invalid task name - $t" >&2
      echo "Available tasks:" >&2
      for x in "${TASK_NAMES[@]}"; do echo "  - $x" >&2; done
      exit 1
    fi
    idx="$(get_config_index_by_task "$t_lc")" || idx=""
    if [[ -z "$idx" ]]; then
      echo "Warning: task '$t' not found in TASK_CONFIGS, will skip" >&2
      continue
    fi
    # de-dupe
    if ! [[ " ${SELECTED_TASK_CONFIG_INDEXES[*]} " =~ " ${idx} " ]]; then
      SELECTED_TASK_CONFIG_INDEXES+=("$idx")
    fi
  done
fi

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
for config_index in "${SELECTED_TASK_CONFIG_INDEXES[@]}"; do
  cfg="${TASK_CONFIGS[config_index]}"
  IFS='|' read -r tname _ _ <<< "$cfg"
  echo "  - $tname"
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
  local config="${TASK_CONFIGS[task_index]}"

  # Parse config
  local name rel_dir fixed_args
  IFS='|' read -r name rel_dir fixed_args <<< "$config"

  local start_time
  start_time="$(date +"%Y-%m-%d %H:%M:%S")"

  local task_dir="${BASE_DIR}/${rel_dir}"
  local model_name_no_spaces="${MODEL_NAME// /}"
  local log_file_name="${name}_${model_name_no_spaces}_${TIMESTAMP}.log"

  echo "----- Start task: $name ($start_time) -----"
  echo "Task dir: $task_dir"

  if [[ ! -d "$task_dir" ]]; then
    echo "Warning: directory not found, skip - $task_dir"
    FAILED_TASKS+=("$name:dir_not_found")
    return 1
  fi

  pushd "$task_dir" &>/dev/null || {
    echo "Warning: unable to cd, skip - $task_dir"
    FAILED_TASKS+=("$name:cd_failed")
    return 1
  }

  mkdir -p "$LOG_DIR_NAME" || {
    echo "Warning: unable to create log dir '$LOG_DIR_NAME', skip"
    FAILED_TASKS+=("$name:mkdir_failed")
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
    echo "Task: $name succeeded [$end_time]"
    COMPLETED_TASKS+=("$name")
  else
    echo "Task: $name failed (exit=$exit_code) [$end_time]"
    FAILED_TASKS+=("$name:exit=$exit_code")
  fi

  popd &>/dev/null
  return $exit_code
}

for task_index in "${SELECTED_TASK_CONFIG_INDEXES[@]}"; do
  run_task "$task_index"
  echo "-------------------------------------"
done

echo "===== End sequential run: $(date +"%Y-%m-%d %H:%M:%S") ====="

