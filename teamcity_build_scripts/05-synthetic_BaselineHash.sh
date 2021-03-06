ROOT_DIR="${PWD}"
cd omniscripts
python3 run_omnisci_benchmark.py --env_name ${ENV_NAME} --env_check True --save_env True --mode synthetic                     \
                                 --ci_requirements ci_requirements.yml                                                        \
                                 --executable "${ROOT_DIR}"/omniscidb/build/bin/omnisci_server                                \
                                 --import-table-name baseline_hash_benchmark --label baseline_hash_test                       \
                                 --port 61274 --name omnisci --user admin --passwd HyperInteractive                           \
                                 -path "${ROOT_DIR}"/omniscidb/Benchmarks                                                     \
                                 --iterations 5 --fragment-size 5000000                                                       \
                                 --synthetic-query BaselineHash --num-fragments 10                                            \
                                 -commit ${BUILD_REVISION}                                                                    \
                                 -db-server ${DATABASE_SERVER_NAME} -db-name "${DATABASE_NAME}" -db-table baselinehashbench   \
                                 -db-user ${DATABASE_USER_NAME} -db-pass "${DATABASE_USER_PW}"
