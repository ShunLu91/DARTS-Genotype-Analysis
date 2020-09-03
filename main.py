import genotypes
from genotype_analysis import GenotypeAnalysis


if __name__ == '__main__':
    Analyzer = GenotypeAnalysis(normal_op=True, reduce_op=True, width_depth=True)

    # analyze single model
    arch = 'NASNet'
    genotype = eval("genotypes.%s" % arch)
    Analyzer.analyze(arch, genotype)

    arch = 'AmoebaNet'
    genotype = eval("genotypes.%s" % arch)
    Analyzer.analyze(arch, genotype)

    arch = 'ENAS'
    genotype = eval("genotypes.%s" % arch)
    Analyzer.analyze(arch, genotype)

    arch = 'DARTS'
    genotype = eval("genotypes.%s" % arch)
    Analyzer.analyze(arch, genotype)

    arch = 'SNAS_MILD'
    genotype = eval("genotypes.%s" % arch)
    Analyzer.analyze(arch, genotype)

    # analyze mixed model
    mix_list = ['NASNet', 'AmoebaNet', 'ENAS', 'DARTS', 'SNAS_MILD']
    mixed_arch = list()
    for _arch in mix_list:
        mixed_arch.append(eval("genotypes.%s" % _arch))
    Analyzer.analyze('mixed_arch', mixed_arch)
