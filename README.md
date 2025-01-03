# What's this?
It's converter EPDE-format differential equations to TEDEouS-format to make TEDEouS solve them. Recently TEDEouS closed support PINN-format equations to solve in its main library, so i needed to convert my EPDE-generated equations to TEDEouS format.
[EPDE](https://github.com/ITMO-NSS-team/EPDE/) is a open-source library from NSS-Lab. This PINN can make stochastic differential equations directly from your data and solve them. 
[TEDEouS](https://github.com/ITMO-NSS-team/torch_DE_solver) is open-source library from NSS-Lab, too. It can solve many types of differential equations, including Burgers equation, wave equations and other. So I choosed this model to solve my equations.  
This model accepts only current-formated dictionaried input.  
My set of functions get DE in string form with params and convert it to dictionary form.  

# Examples
Here I show you one example in [ipynb-file](https://github.com/hellbruh/TEDEouS-EPDE-parser/blob/main/parse_example.ipynb) in current repo

