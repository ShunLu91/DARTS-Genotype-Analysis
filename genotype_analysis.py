import numpy as np
import networkx as nx
from genotypes import PRIMITIVES, Genotype
from utils import print_dict, dict_normalize


class GenotypeAnalysis:
    def __init__(self, normal_op, reduce_op, width_depth):
        """

        :param normal_op: print normal_op analysis or not
        :param reduce_op: print reduce_op analysis or not
        :param width_depth: print width_depth analysis or not
        """
        self.normal_op = normal_op
        self.reduce_op = reduce_op
        self.width_depth = width_depth

        self._initialize()

    def _initialize(self):
        self.normal_dict = {i: 0 for i in PRIMITIVES}
        self.reduce_dict = {i: 0 for i in PRIMITIVES}
        self.geno_info = {
            'normal_width': [], 'normal_width_avg': 0,
            'normal_depth': [], 'normal_depth_avg': 0,
            'reduce_width': [], 'reduce_width_avg': 0,
            'reduce_depth': [], 'reduce_depth_avg': 0
        }
        """

        Args:
            cell: 

        Returns:
            

        """
    def _find_longest_path(self, cell):
        """

        :param cell: a list contains operations and node number such as Genotype.normal or Genotype.reduce
        :return longest_path: : the longest path in the Genotype.normal or Genotype.reduce as defined in Understanding-NAS
        """
        g = nx.OrderedDiGraph()

        g.add_node("c_{k-2}")
        g.add_node("c_{k-1}")
        assert len(cell) % 2 == 0
        steps = len(cell) // 2

        for i in range(steps):
            g.add_node(str(i))

        for i in range(steps):
            for k in [2 * i, 2 * i + 1]:
                op, j = cell[k]
                if j == 0:
                    u = "c_{k-2}"
                elif j == 1:
                    u = "c_{k-1}"
                else:
                    u = str(j - 2)
                v = str(i)
                g.add_edge(u, v, label=op)

        g.add_node("c_{k}")
        for i in range(steps):
            g.add_edge(str(i), "c_{k}")

        longest_path = len(nx.dag_longest_path(g)) - 1

        return longest_path

    def geno_analyze(self, geno):
        """

        :param geno: a standard Genotype in genotypes.py
        :return: None
        """
        if geno.normal:
            normal_width = 0.0
            for op in geno.normal:
                self.normal_dict[op[0]] += 1
                if op[1] in [0, 1]:
                    normal_width += 0.5
            self.geno_info['normal_depth'].append(self._find_longest_path(geno.normal))
            self.geno_info['normal_width'].append(normal_width)
            if len(geno.normal) < 8:
                self.normal_dict['none'] = 8 - len(geno.normal)

        if geno.reduce:
            reduce_width = 0.0
            for op in geno.reduce:
                self.reduce_dict[op[0]] += 1
                if op[1] in [0, 1]:
                    reduce_width += 0.5
            self.geno_info['reduce_depth'].append(self._find_longest_path(geno.reduce))
            self.geno_info['reduce_width'].append(reduce_width)
            if len(geno.reduce) < 8:
                self.reduce_dict['none'] = 8 - len(geno.reduce)

        self.geno_info['normal_width_avg'] = np.round(np.mean(self.geno_info['normal_width']), 1)
        self.geno_info['normal_depth_avg'] = np.round(np.mean(self.geno_info['normal_depth']), 1)
        self.geno_info['reduce_width_avg'] = np.round(np.mean(self.geno_info['reduce_width']), 1)
        self.geno_info['reduce_depth_avg'] = np.round(np.mean(self.geno_info['reduce_depth']), 1)

    def analyze(self, arch, genotype):
        """

        :param arch: name of the analyzed arch
        :param genotype: a standard Genotype in genotypes.py or a genotype list consist of many Genotypes
        :return: None
        """
        self._initialize()

        # analyze
        if isinstance(genotype, list):
            for i, _geno in enumerate(genotype):
                print('mixed_arch_%d' % i, _geno)
                self.geno_analyze(_geno)
        if isinstance(genotype, Genotype):
            print(arch, genotype)
            self.geno_analyze(genotype)

        # print
        if self.normal_op:
            print_dict(dict_normalize(self.normal_dict),
                       sort=True, info='****** %s normal-op ******' % arch, accuracy=3)
        if self.reduce_op:
            print_dict(dict_normalize(self.reduce_dict),
                       sort=True, info='****** %s reduce-op ******' % arch, accuracy=3)
        if self.width_depth:
            print_dict(self.geno_info, info='****** %s genotype-width & depth ******' % arch)
        print('')
