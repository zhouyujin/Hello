#!/bin/bash
set -o pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
BASE_DIR="$SCRIPT_DIR/benchmarks"
LOG_DIR_NAME="logs"

# ================== Global switches ==================
# If TRUE, append pass_data_path to each benchmark (roll-labeled mode).
ROLL_LABELED="FALSE"

# If TRUE, append --use_vl_mode to each benchmark.
USE_VL_MODE="FALSE"

# ================== Model / API config ==================
MODEL_NAME="s1_32b_128k_ckp100_1216"
API_URL="http://10.20.4.4:50001/v1/"
API_KEY="EMPTY"
NUM_WORKERS=150

# ================== Task list (execution order) ==================
TASK_NAMES=(
  "LAB-Bench"
  "GPQA" "AIME24" "AIME25" "LIVE_MATH_BENCH"
  "ChemBench" "Physics"
  "Qiskit_HumanEval" "MaScQA" "MSQA_Long" "MSQA_Short" "SciBench" "ProteinLMbench" "TOMG-Bench" "AMC23"
)

# ================== Task configs ==================
# Format: "DisplayName|BenchmarkDir|Params"
# NOTE:
# - Params should NOT include --model (added centrally).
# - Params SHOULD include --api_url/--api_key/--num_workers if needed.
# - BenchmarkDir must match folder name under $BASE_DIR.
TASK_CONFIGS=(
  "ChemBench|ChemBench|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --num_workers $NUM_WORKERS"
  "gaokao|gaokao|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 5 --num_workers $NUM_WORKERS"
  "GPQA_EvalScope|GPQA_EvalScope|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 8 --num_workers $NUM_WORKERS"
  "GPQA|GPQA|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 8 --num_workers $NUM_WORKERS"
  "LAB-Bench|LAB-Bench|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 7200 --n 1 --num_workers $NUM_WORKERS"
  "LLM-MSE|LLM-MSE|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 8 --judge_api_url https://s1-wjy-resource.openai.azure.com/openai/v1/ --judge_model gpt-4o --judge_api_key F6GuYA0c2MSCn1Fi8CSFa1fzIRrZl79etoUDNrXexpXxdNDg4T1zJQQJ99BFACHYHv6XJ3w3AAAAACOGkoWg --num_workers $NUM_WORKERS"
  "MaScQA|MaScQA|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --judge_api_url https://s1-wjy-resource.openai.azure.com/openai/v1/ --judge_model gpt-4o --judge_api_key F6GuYA0c2MSCn1Fi8CSFa1fzIRrZl79etoUDNrXexpXxdNDg4T1zJQQJ99BFACHYHv6XJ3w3AAAAACOGkoWg --num_workers $NUM_WORKERS"
  "MSQA_Long|MSQA_Long|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --judge_api_url https://s1-wjy-resource.openai.azure.com/openai/v1/ --judge_model gpt-4o --judge_api_key F6GuYA0c2MSCn1Fi8CSFa1fzIRrZl79etoUDNrXexpXxdNDg4T1zJQQJ99BFACHYHv6XJ3w3AAAAACOGkoWg --num_workers $NUM_WORKERS"
  "MSQA_Short|MSQA_Short|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "Physics|Physics|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 1 --judge_api_url https://ark.cn-beijing.volces.com/api/v3/ --judge_api_key 30a70266-37d5-4210-b8a2-34d5fb629230 --judge_model ep-20251110162353-6zqst --num_workers $NUM_WORKERS"
  "Qiskit_HumanEval|Qiskit_HumanEval|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "ProteinLMbench|ProteinLMBench|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "SciBench|SciBench|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "SciEval|SciEval|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "TOMG-Bench|TOMG-Bench|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "UGPhysics|UGPhysics|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 1.0 --timeout 3600 --n 1 --judge_api_url https://ark.cn-beijing.volces.com/api/v3/ --judge_api_key 30a70266-37d5-4210-b8a2-34d5fb629230 --judge_model ep-20251110162353-6zqst --num_workers $NUM_WORKERS"
  "IFEval|IFEval|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 3600 --n 1 --num_workers $NUM_WORKERS"
  "InternalLongtext|InternalLongtext|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 10800 --n 1 --num_workers $NUM_WORKERS"
  "AIME25|MATH|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 18000 --n 16 --task aime25 --num_workers $NUM_WORKERS"
  "AIME24|MATH|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 18000 --n 16 --task aime24 --num_workers $NUM_WORKERS"
  "AMC23|MATH|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 18000 --n 4 --task amc23 --num_workers $NUM_WORKERS"
  "LIVE_MATH_BENCH|MATH|--api_url $API_URL --api_key $API_KEY --temperature 0.6 --top_p 0.95 --presence_penalty 0.0 --timeout 18000 --n 4 --task live_math_bench --num_workers $NUM_WORKERS"
)

show_help() {
  echo "Usage: $0 [task_number ...]"
  echo "Run benchmark tasks sequentially. If no task number is given, run all tasks."
  echo
  echo "Examples:"
  echo "  Run all tasks:     $0"
  echo "  Run task 1 and 3:  $0 1 3"
  echo "  Show help:         $0 -h | $0 --help"
  echo
  echo "Available tasks:"
  for i in "${!TASK_NAMES[@]}"; do
    echo "  $((i+1)). ${TASK_NAMES[i]}"
  done
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  show_help
  exit 0
fi

SELECTED_TASK_ORIGINAL_INDEXES=()
if [[ $# -eq 0 ]]; then
  for i in "${!TASK_NAMES[@]}"; do
    SELECTED_TASK_ORIGINAL_INDEXES+=("$i")
  done
else
  for task_num in "$@"; do
    if ! [[ "$task_num" =~ ^[0-9]+$ ]]; then
      echo "Error: task number must be numeric - $task_num" >&2
      exit 1
    fi
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
echo
echo "Tasks to run:"
for original_index in "${SELECTED_TASK_ORIGINAL_INDEXES[@]}"; do
  task_num=$((original_index + 1))
  task_name="${TASK_NAMES[original_index]}"
  echo "  $task_num. $task_name"
done
echo "----------------------------------------"

run_task() {
  local task_index="$1"
  local original_index="$2"
  local display_num=$((original_index + 1))
  local config="${TASK_CONFIGS[task_index]}"

  # Parse config
  local name rel_dir params
  IFS='|' read -r name rel_dir params <<< "$config"

  local start_time
  start_time="$(date +"%Y-%m-%d %H:%M:%S")"

  # Model-specific tweaks
  if [[ "$MODEL_NAME" == "gpt-4" ]]; then
    echo "Warning: GPT-4 may not support multi-turn, appending --single_turn"
    params="${params} --single_turn"
  fi

  if [[ "$ROLL_LABELED" == "TRUE" ]]; then
    params="${params} --pass_data_path '/data02/home/zdhs0075/benchmark_suite/Rolldata1015/test_outputs_good/${rel_dir}.json'"
  fi
  if [[ "$USE_VL_MODE" == "TRUE" ]]; then
    params="${params} --use_vl_mode"
  fi

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
  local cmd="python -u run.py --model $MODEL_NAME $params > $log_path 2>&1"
  echo "Command: $cmd"
  echo "Log: $log_path"

  eval "$cmd"
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

