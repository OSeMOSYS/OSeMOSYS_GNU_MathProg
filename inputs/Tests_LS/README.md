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
Growing gas demand 2020-22 500 - 23-25 1000
TotalAnnualMaxCapacityInvestment: 50MW for all


# test 4

test 3 +:
    retiring capacity: gas plant -100 MW in 2022 -100 MW in 2024
                        solar and bio -50 in 2024
    capital and O&M costs power plants

# test 5

test 4 + Add disaggregated end use demand for transport

new fuel: gasoline, diesel, tra_car 

new tech: imp_gsl, imp_dsl. car_gsl, car_dsl 

# test 6

test 5 + growing demand transport and competition car_gsl vs car_dsl

deamand tra_car 1000 1500 2000 ...

            capitalcost     fuelcost
car_gsl         15              1.5
car_dsl         20              1

TotalAnnualMaxCapacityInvestment: 400 each    

# test 7 

test 6 + add bus and disaggregate demand tra_car

new fuel: tra_bus, tra_land
new tech: bus, tra_bus, tra_car

1 bus = 10 passengers

efficiency = 1/9
tra_bus = 10 tra_land
bus - capital cost = 200 - residual capacity = 100 - maxcapinvestment = 10

demand tra_land = 2000 2500 3000 ...

# test 8

test 7 + minimum and maximum investment and activity limits

car_dsl:
    TotalAnnualMinCapacityInvestment 10 10 10 10 10 10
    TotalTechnologyAnnualActivityLowerLimit 500 600 700 800 900 1000
car_gsl:
    TotalAnnualMaxCapacity ... 2025 2401
    TotalTechnologyAnnualActivityUpperLimit 600 800 1200 1500 2000 2500
tra_bus:
    TotalTechnologyAnnualActivityUpperLimit 110 110 115 120 125 130 
