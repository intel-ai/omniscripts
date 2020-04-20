import argparse
import os
import re

from .utils import DataFileParser, KeyValueListParser, str_arg_to_bool
from environment import create_conda_env
from server import OmnisciServer


def add_mysql_arguments(parser):
    mysql = parser.add_argument_group("mysql")

    mysql.add_argument(
        "-db_server", dest="db_server", default="localhost", help="Host name of MySQL server."
    )
    mysql.add_argument(
        "-db_port", dest="db_port", default=3306, type=int, help="Port number of MySQL server."
    )
    mysql.add_argument(
        "-db_user",
        dest="db_user",
        help="Username to use to connect to MySQL database. "
        "If user name is specified, script attempts to store results in MySQL "
        "database using other -db-* parameters.",
    )
    mysql.add_argument(
        "-db_pass",
        dest="db_pass",
        default="omniscidb",
        help="Password to use to connect to MySQL database.",
    )
    mysql.add_argument(
        "-db_name",
        dest="db_name",
        default="omniscidb",
        help="MySQL database to use to store benchmark results.",
    )
    mysql.add_argument(
        "-db_table_etl",
        dest="db_table_etl",
        help="Table to use to store ETL results for this benchmark.",
    )
    mysql.add_argument(
        "-db_table_ml",
        dest="db_table_ml",
        help="Table to use to store ML results for this benchmark.",
    )


def add_omnisci_arguments(parser):
    omnisci = parser.add_argument_group("omnisci")

    omnisci.add_argument(
        "-executable", dest="executable", required=True, help="Path to omnisci_server executable."
    )
    omnisci.add_argument(
        "-omnisci_cwd",
        dest="omnisci_cwd",
        help="Path to omnisci working directory. "
        "By default parent directory of executable location is used. "
        "Data directory is used in this location.",
    )
    omnisci.add_argument(
        "-port",
        dest="port",
        default=None,
        type=int,
        help="TCP port number to run omnisci_server on.",
    )
    omnisci.add_argument(
        "-http_port",
        dest="http_port",
        default=None,
        type=int,
        help="HTTP port number to run omnisci_server on.",
    )
    omnisci.add_argument(
        "-calcite_port",
        dest="calcite_port",
        default=None,
        type=int,
        help="Calcite port number to run omnisci_server on.",
    )
    omnisci.add_argument(
        "-user", dest="user", default="admin", help="User name to use for omniscidb server."
    )
    omnisci.add_argument(
        "-password",
        dest="password",
        default="HyperInteractive",
        help="User password to use for omniscidb server.",
    )
    omnisci.add_argument(
        "-database_name",
        dest="database_name",
        default="agent_test_ibis",
        help="Database name to use for omniscidb server.",
    )
    omnisci.add_argument(
        "-debug_timer",
        dest="debug_timer",
        default=False,
        type=str_arg_to_bool,
        help="Enable fine-grained query execution timers for debug.",
    )
    omnisci.add_argument(
        "-columnar_output",
        dest="columnar_output",
        default=None,
        type=str_arg_to_bool,
        help="Allows OmniSci Core to directly materialize intermediate projections \
            and the final ResultSet in Columnar format where appropriate.",
    )
    omnisci.add_argument(
        "-lazy_fetch",
        dest="lazy_fetch",
        default=None,
        type=str_arg_to_bool,
        help="[lazy_fetch help message]",
    )
    omnisci.add_argument(
        "-multifrag_rs",
        dest="multifrag_rs",
        default=None,
        type=str_arg_to_bool,
        help="[multifrag_rs help message]",
    )
    omnisci.add_argument(
        "-omnisci_run_kwargs",
        dest="omnisci_run_kwargs",
        default={},
        metavar="KEY1=VAL1,KEY2=VAL2...",
        action=KeyValueListParser,
        help="additional options to pass when starting omnisci server",
    )
    omnisci.add_argument(
        "-commit_omnisci",
        dest="commit_omnisci",
        default="1234567890123456789012345678901234567890",
        help="Omnisci commit hash to use for tests.",
    )


def add_ibis_arguments(parser):
    ibis = parser.add_argument_group("ibis")

    ibis.add_argument(
        "-expression",
        dest="expression",
        default=" ",
        help="Run tests which match the given substring test names and their parent "
        "classes. Example: 'test_other', while 'not test_method' matches those "
        "that don't contain 'test_method' in their names.",
    )
    ibis.add_argument(
        "-commit_ibis",
        dest="commit_ibis",
        default="1234567890123456789012345678901234567890",
        help="Ibis commit hash to use for tests.",
    )


def add_benchmark_arguments(parser, supported_benchmarks):
    benchmark = parser.add_argument_group("benchmark")

    benchmark.add_argument(
        "-bench_name", dest="bench_name", choices=supported_benchmarks, help="Benchmark name."
    )
    benchmark.add_argument(
        "-data_file",
        dest="data_file",
        action=DataFileParser,
        help="A datafile that should be loaded.",
    )
    benchmark.add_argument(
        "-dfiles_num",
        dest="dfiles_num",
        default=1,
        type=int,
        help="Number of datafiles to input into database for processing.",
    )
    benchmark.add_argument(
        "-iterations",
        dest="iterations",
        default=1,
        type=int,
        help="Number of iterations to run every query. Best result is selected.",
    )
    benchmark.add_argument(
        "-dnd", default=False, type=str_arg_to_bool, help="Do not delete old table."
    )
    benchmark.add_argument(
        "-dni",
        default=False,
        type=str_arg_to_bool,
        help="Do not create new table and import any data from CSV files.",
    )
    benchmark.add_argument(
        "-validation",
        dest="validation",
        default=False,
        type=str_arg_to_bool,
        help="validate queries results (by comparison with Pandas queries results).",
    )
    benchmark.add_argument(
        "-import_mode",
        dest="import_mode",
        default="fsi",
        choices=["copy-from", "pandas", "fsi"],
        help="mode to read datasets",
    )
    benchmark.add_argument(
        "-optimizer",
        choices=["intel", "stock"],
        dest="optimizer",
        default="intel",
        help="Which optimizer to use",
    )
    benchmark.add_argument(
        "-no_ibis",
        default=False,
        type=str_arg_to_bool,
        help="Do not run Ibis benchmark, run only Pandas (or Modin) version",
    )
    benchmark.add_argument(
        "-no_pandas",
        default=False,
        type=str_arg_to_bool,
        help="Do not run Pandas version of benchmark",
    )
    benchmark.add_argument(
        "-pandas_mode",
        choices=["Pandas", "Modin_on_ray", "Modin_on_dask", "Modin_on_python"],
        default="Pandas",
        help="Specifies which version of Pandas to use.",
    )
    benchmark.add_argument(
        "-ray_tmpdir",
        default="/tmp",
        help="Location where to keep Ray plasma store. "
        "It should have enough space to keep -ray_memory",
    )
    benchmark.add_argument(
        "-ray_memory",
        default=200 * 1024 * 1024 * 1024,
        help="Size of memory to allocate for Ray plasma store",
    )
    benchmark.add_argument(
        "-no_ml",
        default=False,
        type=str_arg_to_bool,
        help="Do not run machine learning part, run only ETL part",
    )
    benchmark.add_argument(
        "-gpu_memory",
        dest="gpu_memory",
        type=int,
        help="specify the memory of your gpu, default 16. "
        "(This controls the amount of lines to be used. Also work for CPU version. )",
        default=16,
    )
    benchmark.add_argument(
        "-fragments_size",
        dest="fragments_size",
        default=None,
        nargs="*",
        type=int,
        help="Number of rows per fragment that is a unit of the table for query processing. \
            Should be specified for each table in workload",
    )
    benchmark.add_argument(
        "-table",
        dest="table",
        default="benchmark_table",
        help="Table name name to use for omniscidb server.",
    )
    benchmark.add_argument(
        "-ipc_conn",
        dest="ipc_connection",
        default=True,
        type=str_arg_to_bool,
        help="Connection type for ETL operations",
    )


def add_omniscript_arguments(omniscript, omniscript_path):
    omniscript.add_argument(
        "-i", "--ibis_path", dest="ibis_path", required=True, help="Path to ibis directory."
    )

    # Setup environment
    omniscript.add_argument(
        "-en", "--env_name", dest="env_name", required=True, help="Conda env name."
    )
    omniscript.add_argument(
        "-ec",
        "--env_check",
        dest="env_check",
        default=False,
        type=str_arg_to_bool,
        help="Check if env exists. If it exists don't recreate.",
    )
    omniscript.add_argument(
        "-s",
        "--save_env",
        dest="save_env",
        default=False,
        type=str_arg_to_bool,
        help="Save conda env after executing.",
    )
    omniscript.add_argument(
        "-py",
        "--python_version",
        dest="python_version",
        default="3.7",
        choices=["3.6", "3.7"],
        help="File with ci requirements for conda env.",
    )
    omniscript.add_argument(
        "-ci",
        "--ci_requirements",
        dest="ci_requirements",
        default=os.path.join(omniscript_path, "ci_requirements.yml"),
        help="File with ci requirements for conda env.",
    )


def create_cli(omniscript_path, supported_benchmarks):
    omniscript = argparse.ArgumentParser(description="omniscript cli")
    add_omniscript_arguments(omniscript, omniscript_path)

    subparsers = omniscript.add_subparsers(required=True, help="sub-command help")

    parser_build = subparsers.add_parser("build", help="build help")
    parser_build.set_defaults(func=build)

    parser_ibis_test = subparsers.add_parser("test", help="test ibis help")
    parser_ibis_test.set_defaults(func=ibis_test)
    add_ibis_arguments(parser_ibis_test)
    add_omnisci_arguments(parser_ibis_test)
    parser_ibis_test.add_argument(
        "-r",
        "--report_path",
        dest="report_path",
        default=os.path.join(omniscript_path, ".."),
        help="Path to report file.",
    )

    parser_benchmark = subparsers.add_parser("benchmark", help="build help")
    # hack
    parser_benchmark.set_defaults(
        func=benchmark, omniscript_path=omniscript_path, interface=omniscript
    )
    add_benchmark_arguments(parser_benchmark, supported_benchmarks)
    add_mysql_arguments(parser_benchmark)
    add_omnisci_arguments(parser_benchmark)

    return omniscript


def build(args):
    with create_conda_env(
        args.ibis_path,
        args.env_name,
        args.env_check,
        args.env_save,
        args.python_version,
        args.ci_requirements,
    ) as conda_env:

        print("IBIS INSTALLATION")
        install_ibis_cmdline = ["python3", os.path.join("setup.py"), "install"]
        conda_env.run(install_ibis_cmdline, cwd=args.ibis_path, print_output=False)


def ibis_test(args):
    with create_conda_env(
        args.ibis_path,
        args.env_name,
        args.env_check,
        args.env_save,
        args.python_version,
        args.ci_requirements,
    ) as conda_env:

        ibis_data_script = os.path.join(args.ibis_path, "ci", "datamgr.py")

        report_file_name = f"report-{args.commit_ibis[:8]}-{args.commit_omnisci[:8]}.html"
        if not os.path.isdir(args.report_path):
            os.makedirs(args.report_path)
        report_file_path = os.path.join(args.report_path, report_file_name)

        print("STARTING OMNISCI SERVER")
        with OmnisciServer(
            omnisci_executable=args.executable,
            omnisci_port=args.port,
            http_port=args.http_port,
            calcite_port=args.calcite_port,
            database_name=args.database_name,
            omnisci_cwd=args.omnisci_cwd,
            user=args.user,
            password=args.password,
            debug_timer=args.debug_timer,
            columnar_output=args.columnar_output,
            lazy_fetch=args.lazy_fetch,
            multifrag_rs=args.multifrag_rs,
            omnisci_run_kwargs=args.omnisci_run_kwargs,
        ) as omnisci_server_launched:

            print("DOWNLOADING DATA")
            dataset_download_cmdline = ["python3", ibis_data_script, "download"]
            conda_env.run(dataset_download_cmdline)

            print("IMPORTING DATA BY OMNISCI")
            dataset_import_cmdline = [
                "python3",
                ibis_data_script,
                "omniscidb",
                "-P",
                str(omnisci_server_launched.server_port),
                "--database",
                args.database_name,
            ]
            conda_env.run(dataset_import_cmdline)

            print("RUNNING TESTS")
            ibis_tests_cmdline = [
                "pytest",
                "-m",
                "omniscidb",
                "--disable-pytest-warnings",
                "-k",
                args.expression,
                f"--html={report_file_path}",
            ]

            os.environ["IBIS_TEST_OMNISCIDB_DATABASE"] = args.database_name
            os.environ["IBIS_TEST_DATA_DB"] = args.database_name
            os.environ["IBIS_TEST_OMNISCIDB_PORT"] = str(omnisci_server_launched.server_port)
            # pytest depends on above env variables
            conda_env.run(ibis_tests_cmdline, cwd=args.ibis_path)


def benchmark(args):
    with create_conda_env(
        args.ibis_path,
        args.env_name,
        args.env_check,
        args.env_save,
        args.python_version,
        args.ci_requirements,
    ) as conda_env:

        benchmark_script_path = os.path.join(args.omniscript_path, "run_ibis_benchmark.py")
        benchmark_cmd = ["python3", benchmark_script_path]

        possible_benchmark_args = [
            "bench_name",
            "data_file",
            "dfiles_num",
            "iterations",
            "dnd",
            "dni",
            "validation",
            "optimizer",
            "no_ibis",
            "no_pandas",
            "pandas_mode",
            "ray_tmpdir",
            "ray_memory",
            "no_ml",
            "gpu_memory",
            "db_server",
            "db_port",
            "db_user",
            "db_pass",
            "db_name",
            "db_table_etl",
            "db_table_ml",
            "executable",
            "omnisci_cwd",
            "port",
            "http_port",
            "calcite_port",
            "user",
            "password",
            "ipc_conn",
            "database_name",
            "table",
            "commit_omnisci",
            "commit_ibis",
            "import_mode",
            "debug_timer",
            "columnar_output",
            "lazy_fetch",
            "multifrag_rs",
            "fragments_size",
            "omnisci_run_kwargs",
        ]
        args_dict = vars(args)
        for arg_name in list(args.interface._option_string_actions.keys()):
            try:
                pure_arg = re.sub(r"^--*", "", arg_name)
                if pure_arg in possible_benchmark_args:
                    arg_value = args_dict[pure_arg]
                    # correct filling of arguments with default values
                    if arg_value is not None:
                        if isinstance(arg_value, dict):
                            if arg_value:
                                benchmark_cmd.extend(
                                    [
                                        arg_name,
                                        ",".join(
                                            f"{key}={value}" for key, value in arg_value.items()
                                        ),
                                    ]
                                )
                        elif isinstance(arg_value, (list, tuple)):
                            if arg_value:
                                benchmark_cmd.extend([arg_name] + [str(x) for x in arg_value])
                        else:
                            benchmark_cmd.extend([arg_name, str(arg_value)])

            except KeyError:
                pass

        print(benchmark_cmd)
        conda_env.run(benchmark_cmd)
