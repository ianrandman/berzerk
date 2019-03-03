import pickle


class Network(object):
    def __init__(self, inputs, outputs, node_evals):
        self.input_nodes = inputs
        self.output_nodes = outputs
        self.node_evals = node_evals
        self.values = dict((key, 0.0) for key in inputs + outputs)

    def activate(self, inputs):
        if len(self.input_nodes) != len(inputs):
            raise RuntimeError("Expected {0:n} inputs, got {1:n}".format(len(self.input_nodes), len(inputs)))

        for k, v in zip(self.input_nodes, inputs):
            self.values[k] = v

        for node, act_func, agg_func, bias, response, links in self.node_evals:
            node_inputs = []
            for i, w in links:
                node_inputs.append(self.values[i] * w)
            s = agg_func(node_inputs)
            self.values[node] = act_func(bias + response * s)

        return [self.values[i] for i in self.output_nodes]


def load_network(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
        input_nodes = data[0]
        output_nodes = data[1]
        node_evals = data[2]
        return Network(input_nodes, output_nodes, node_evals)


def save_network(net, filename):
    with open(filename, "wb") as f:
        pickle.dump([net.input_nodes, net.output_nodes, net.node_evals], f)
