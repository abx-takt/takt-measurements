# What we have already sped up

Every line below is a real program that people wait for. We ran it on our test machine the normal
way and our way, timed the whole job from start to finish both ways, and compared the results with
the original. The numbers say how many times sooner the job finished: 2 times means the job took
half as long. Each line links to a page with the full details: which program and version, what
exactly we ran, and how you can check it yourself.

| What you run | What changes between runs | How much sooner the job finished | The results | Details |
|---|---|---|---|---|
| Reports on tree models: which features matter, what-if questions (XGBoost, scikit-learn, CatBoost) | the question you ask the model | 2 to 10 times, by report (6.75×, 4.26×, 3.24×, 9.98×, 5.08×, 2.24×, 1.92×) | every number identical | [Tree-model reports](https://taktcycles.com/showcase/tree-explanations/README.html); [LightGBM, measured separately](https://taktcycles.com/showcase/lightgbm/README.html) |
| Strategy backtests and parameter searches (vn.py, backtrader, freqtrade, TA-Lib) | the parameters you try | 2 to 16 times, by case (vn.py 16.3×; backtrader 2.24–5.23×; freqtrade 5.91–11.02×; one TA-Lib indicator 7.11×) | the same answers | [Strategy grids](https://taktcycles.com/showcase/strategy-grids/README.html) |
| Option pricing with Monte Carlo (QuantLib) | the options you price | 22.8 times on one pricing job | identical to the last digit | [Strategy grids](https://taktcycles.com/showcase/strategy-grids/README.html) |
| Radiation shielding: trying different materials (OpenMC) | the density of one material | 3.55 times for ten scenarios (3.79 times against ten separate command-line runs) | the same physics results | [Simulation families](https://taktcycles.com/showcase/simulation-families/README.html) |
| Noise maps: trying different barriers (NoiseModelling) | the barrier’s height, position or length, one at a time (three separate studies) | 2.54, 2.37 and 2.39 times for ten scenarios each | identical files | [Simulation families](https://taktcycles.com/showcase/simulation-families/README.html) |
| Building models: checking clashes after moving parts (IfcClash) | where the parts are | 2.23 times for ten scenarios | the same clash list | [Simulation families](https://taktcycles.com/showcase/simulation-families/README.html) |
| Sunlight on terrain after editing the map (GRASS GIS r.sun) | a patch of the terrain | 2.38 times for ten scenarios | identical files | [Simulation families](https://taktcycles.com/showcase/simulation-families/README.html) |
| Genome scans after a change in the reference (Cas-OFFinder) | a stretch of the reference sequence | 5.77 times on chromosome 1; 6.07 times on chromosome 2 in a separate study; ten scenarios each | the same hits | [Sequence search](https://taktcycles.com/showcase/sequence-families/README.html) |
| Structures: many loads on one model (CalculiX) | the loads | 2.72 times for ten loads on a test model; 1.47 times on one real model from a public dataset | identical files, apart from the run time stamps | [Load cases](https://taktcycles.com/showcase/fea-loadcase-families/README.html) |
| Cleaning large 3D microscope images (SciPy) | a small region of the image | 6.96 times on a test image, 6.97 times on real microscopy data, ten edits each | identical images | [Volume morphology](https://taktcycles.com/showcase/volume-morphology-families/README.html) |

## How to read the numbers

- “Times sooner” is the whole job, start to finish, on the same machine: the normal way divided by our way. Nothing is left out of our side, including the first full calculation when we need one.
- Most figures divide the total time of the whole job the normal way by the total time our way. Some compare the typical (median) time of repeated runs. Each page says which, and shows every reading.
- “The results” means we compared what came out, not just how long it took. “Identical” means every byte. “The same” means the same complete answer after sorting, or after leaving out fields that change on every run anyway, such as time stamps. Each page says exactly what was compared.
- The numbers say how much sooner the same answer arrived, and nothing else: not whether a model is accurate or a strategy profitable.
- A number applies to the program and the job on its page. Your program is measured on its own job before we promise anything.
- The programs and data belong to their authors and keep their licences. We publish readings, not software.

## Your program

[Tell us what you run](https://taktcycles.com/?src=showcase-measured-classes#start): which program, how big the job is, how often you run it and how long you wait. The first check is free, and you pay only if your job got faster.
