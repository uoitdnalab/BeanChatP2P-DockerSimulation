# BeanChatP2P-DockerSimulation

Build and run
-------------

Modify `CHECK_NODES` variable in `get_timing_info.py` to match network
dimensions.

```
./auto_docker_deploy_auto_test.sh NETWORK_ROWS NETWORK_COLS

python generate_netfilter_rules.py NETWORK_ROWS NETWORK_COLS

chmod u+x apply_netfilter_rules.sh

chmod u+x remove_netfilter_rules.sh

./apply_netfilter_rules.sh

./run_dockers.sh
```

Cleanup
-------

```
./killall.sh
./remove_netfilter_rules.sh

rm -rf __build
rm -rf __mounts
```
