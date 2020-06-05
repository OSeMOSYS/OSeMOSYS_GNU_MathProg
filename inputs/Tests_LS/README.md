### quick description of the model tested

# test1

Contains one simple power sector model, fixed demand, fixed capacity (no new investment)

timesplit 2 Day Night

demand 1000 GWh

Supply:             Capacity    Efficiency  CapacityFactor
        GasTurbine   300MW          1/3             50%
        BiomassPlant 100MW          1/3             30%
        SolarPV      100MW           1       30%(day)0(night) 

Fuels:              FuelCost
    Biomass             1
    Electricity
    Gas                 3
    Solar

Mining:
        GasExtraction
        BiomassExtraction
        Sun    

### result
minor differences due to roundings

# test2

Same as test1 + Gas demand from residential sector

demand
    Gad_res 500 GWh

New technology:
    GasGrid efficiency 1/1.1


# test3

Growing electricity demand 1000, 1500, 2000 ...

TotalAnnualMaxCapacityInvestment: 20MW for all
