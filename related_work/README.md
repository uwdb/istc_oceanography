

## Science: Structure and function of the global ocean microbiome
[Original link, May 2015](http://science.sciencemag.org/content/348/6237/1261359).
[Supplemental table of sample locations and sources](http://science.sciencemag.org/content/suppl/2015/05/20/348.6237.1261359.DC1).

Major takeaways:

* **Temperature** is the strongest environmental factor explaining microbial community diversity. 
The temperature "sweet spot" for maximum diversity is 12-13 Celsius.
* **Depth** strongly correlates with microbial community diversity. 
The samples taken at lower depths have greater diversity.
As expected, cell density (i.e., number of genes per cubic meter) and growth rate decrease at lower depths.
* Dissimilarity increases with **horizontal distance** between sample locations. 
This finding supports the hypothesis that the ocean's microbes have distinct geographic communities/clusters, as opposed to one big homogeneous distribution of microbes that just vary with temperature.
* Weak to no correlation with oxygen, salinity, and other nutrients. 
Oxygen is tightly correlated with temperature. They trained two [*elastic net*](https://en.wikipedia.org/wiki/Elastic_net_regularization) ML models, one on temperature and another on oxygen, to distinguish their relationship with diversity. The ML model for temperature held predictive power across depth levels, while the ML model for oxygen did not generalize.
* A *comparison to the genetic data from the human gut* shows a large (~70%) "core" of genes that are abundant in both in the human gut and the ocean.  ~12% of the genes in the human gut and ~12% in the ocean were unique to that environment. 

By "microbial community diversity", I refer to the distribution of identified genes (taxonomic diversity) and to the distribution of identified genes grouped by their function (functional diversity).


Techniques and datasets:

* Used "metagenomic assembly and gene prediction" techniques alongside public reference genomes to reconstruct the genomic content. The result is the [**OM-RGC** database](http://ocean-microbiome.embl.de/companion.html).
* Heavy use of **Principal Coordinate Analysis** (different from PCA; see the [PCoA folder](PCoA/)) as well as Bray-Curtis dissimilarity.
* Looks like most work took place in R and Python's scikit-learn.




Potential analysis:

```
(SampleID, temperature, 1)^T x (SampleID, k-mer, frequency)
= (temperature, k-mer, frequency)
Then compare the k-mer profile across temperatures.
```
