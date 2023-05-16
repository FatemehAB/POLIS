
from BUS import *

def run_config(config_params, i, dirName, dirsave, POLIS_detail):
    best_prog = None
    best_reward = -1000
    agent_num = i

    times = [time.time()]
    interactions = [0]
    performances = []
    stds = []
    collisions = []
    numberOfPrograms = []
    ids_order = []

    from DQN.evaluation import collecting_data

    observations, actions, n_interactions = collecting_data(config_params['path_to_agent']+str(agent_num)+"/", str(agent_num), config_params['env_name'], config_params['highlight'])

    times.append(time.time())
    interactions.append(n_interactions)

    from node_visitor import AnalysisNodeVisitor
    import ast
    with open(config_params["filename"]) as f:
        tree = ast.parse(f.read())
    v = AnalysisNodeVisitor()
    program = v.visit(tree)
    heu = []
    for p in program:
        if isinstance(p, Node):
            heu.append(p)

    heuristic = Function(heu, obs = observations, acts=actions)
    heuristic.set_IDs()



    pre_performance, pre_std, n_collision, inter = heuristic.evaluate(config_params["n_episodes"], env_name=config_params["env_name"])
    n_interactions+=inter

    times.append(time.time())
    interactions.append(n_interactions)
    performances.append(pre_performance)
    numberOfPrograms.append(0)
    stds.append(pre_std)
    ids_order.append(-1)

    print("Initial average reward, std, and the number of collisions of heuristic function:")
    print(str(pre_performance) + " , "+ str(pre_std)+ " , "+str(n_collision))
    print(pre_performance)

    start = time.time()

    while (time.time() - start < config_params["total_time"]):
        y, z, id, t, k, c, p = heuristic.improve_function(pre_performance, config_params["observation"], config_params["action"], max_time=config_params["max_time"], bound=config_params["synthesis_size"],
                                                          total_time=config_params['total_time'], start_time=start, env_name=config_params["env_name"] ,
                                                          initial_interaction=n_interactions, pre_collisions=n_collision, t_n_p=numberOfPrograms[-1], ops=POLIS_detail)
        times += t
        performances += y
        interactions+= k
        collisions+=c
        numberOfPrograms+=p
        ids_order+=id

        if len(y) > 0:
            pre_performance = y[-1]
        if len(k) > 0:
            n_interactions = k[-1]
        if len(c) > 0:
            n_collision = c[-1]


    print("After improvement average reward, std, and the number of collisions of heuristic function:")
    print(str(pre_performance) + " , " + str(n_collision))

    with open(dirsave + config_params["plot_name"] + "/" + dirName + "/results_" + str(
            config_params["max_time"]) + str(i) + ".txt", 'a') as results:
        results.write("mean and std reward and collisions and total interactions: " + str(pre_performance) + " , " + str(n_collision)+ " , "+ str(interactions[-1]) +"\n")

    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/times_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", times)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/performance_by_time_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", performances)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/interactions_by_time_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", interactions)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/number_of_programs_by_time_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", numberOfPrograms)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/collisions_by_time_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", collisions)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/ids_by_time_" + str(config_params["max_time"]) + "_" + str(agent_num) + ".npy", ids_order)
    np.save(dirsave + config_params["plot_name"] + "/" + dirName + "/final_heuristic" + "_" + str(agent_num) + ".npy", heuristic)


    if pre_performance > best_reward:
        best_reward = pre_performance
        best_prog = heuristic

    with open(dirsave + config_params["plot_name"] + "/" + dirName + "/program_" + str(
            config_params["max_time"]) + str(i) + ".txt", 'a') as results:
        results.write("best program\n")
        results.write(best_prog.to_string() + "\n")



if __name__ == '__main__':
    import warnings

    warnings.filterwarnings("ignore")

    import argparse

    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Optional app description')

    parser.add_argument('--path_to_config')
    parser.add_argument('--agent_num')
    parser.add_argument('--dirsave')

    args = parser.parse_args()

    with open(args.path_to_config) as config_json_file:
        config_params = json.load(config_json_file)

    import os

    dirName = date.today().strftime("%b-%d-%Y")
    try:
        os.makedirs(args.dirsave + config_params["plot_name"] + "/" + dirName)
    except FileExistsError:
        print("Directory ", dirName, " already exists")

    POLIS_detail = {"Att_Var": [Multiplication, Addition, Subtraction, Division, Variable, Num],
                       "Att_Ite": [Multiplication, Addition, Subtraction, Division, Lt, Gt, And, Or, Equal, Lt_Eq,
                                   Gt_Eq, NotEqual, Variable, Num],
                    "constants": [0.1],
                    }


    run_config(config_params, args.agent_num, dirName, dirsave=args.dirsave, POLIS_detail=POLIS_detail)

