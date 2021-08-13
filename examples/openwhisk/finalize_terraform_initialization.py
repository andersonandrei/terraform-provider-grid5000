import os
import subprocess
import sys

"""
Uses kind_cluster to set up Kubernetes. Then, label and retrieve the master node to return as output.
"""
def set_up_kubernetes(kind_cluster):

    # Export KUBECONFIG value
    os.system("export KUBECONFIG=${PWD}/" + kind_cluster)

    # Wait a bit for the cluster to get ready
    os.system("sleep 2m")

    # Label nodes and prepare to deploy openwhisk
    commands = [
        "kubectl label nodes --all openwhisk-role=invoker"
        "kubectl -n openwhisk wait --for=condition=complete job/ow-install-packages"
        "kubectl -n openwhisk get pods,pvc,job,svc"
    ]
    for cmd in commands:
        os.system(cmd)

    # Retrieve the master node to send to Openwhisk
    cmd = "kubectl get nodes"
    cmd_result = subprocess.getoutput(cmd)
    list_of_nodes = cmd_result.split("\n")
    master_node = list_of_nodes[1].split(" ")[0]

    return master_node


"""
Uses master_node to set up Openwhisk with the correct credentials.
"""
def set_up_openwhisk(master_node):
    commands = [
        "wsk property set --apihost https://" + str(master_node) + ":31001"
        "wsk property set --auth 23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP"
        "wsk --insecure package list /whisk."
    ]
    for cmd in commands:
        os.system(cmd)

    return


"""
Print the parameters of this script.
"""
def print_parameters():
    str = "\nPlease, use one of the following parameters: \n\
    -h                 | help \n\
    -r <kube_config_cluster.yml> | set up Kubernetes with kube_config_cluster.yaml and prepare Openwhisk\n"

    print(str)
    return


def main():
    argvs = sys.argv
    if (len(argvs) == 1):
        print_parameters()
        return

    else:
        if(argvs[1] == "-h"):
           print_parameters()
        elif(argvs[1] == "-r"):
            if (len(argvs) < 3):
                print_parameters()
            else:
                print("Finalizing terraform initialization. Using: " + str(argvs[2]))
                run_exp(argvs[2])
                cluster_config_file = str(argvs[2])
                master_node = set_up_kubernetes(cluster_config_file)
                set_up_openwhisk(master_node)
                print("Finished. Kubernetes master node is: " +  master_node)

main()
