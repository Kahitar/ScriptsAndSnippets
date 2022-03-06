function task_run() {
    pipenv run python application.py -p dev
}

function task_install() {
    pipenv --rm
    pipenv install
}

function task_test() {
    pipenv run python -W ignore::DeprecationWarning test.py
}

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' | sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
fi