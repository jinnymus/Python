#!/usr/bin/env bash

cd /nis-test/pytest/pytests/lib
python setup.py sdist --dist-dir /tmp
pip install -I /tmp/nistest-0.5.tar.gz
cd /nis-test/pytest
/nis-test/pytest/bin/create_connect.sh

#py.test -p no:cacheprovide /nis-test/pytests/

echo 'testing service: '$1

#testrail="  --testrail --tr-url=http://10.97.51.19/testrail/ --tr-email=kalistratovka@nis-glonass.ru --tr-password=*"

case $1 in
    'drs')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_drs_operations.py -s --alluredir report  $testrail --tr-plan-id=5 | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'hds')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_hds_errors.py -s --alluredir report $testrail --tr-plan-id=4 | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        #py.test -p no:cacheprovide -vvrxXs pytests/farming/cases/test_sf_hds_operations.py -s --alluredir report $testrail --tr-plan-id=4 | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'info')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_info_operations.py -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'e2e')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_e2e_operations.py -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'db')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_db_operations.py -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'kafka')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_kafka.py -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'validator')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/farming/cases/test_sf_validator_operations.py -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
    'external')
        py.test -p no:cacheprovide -vvrxXs /nis-test/pytest/pytests/external/* -s --alluredir report | grep -v 'conn.py' | grep -v 'fetcher.py' | grep -v 'metrics.py' | grep -v 'client_async.py'
        ;;
esac