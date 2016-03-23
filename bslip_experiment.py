import tools
import basic_model

b0 = tools.load_nolan_bedrock()
obs_surf = tools.load_first_guess_surface()

start = [.001, .001125, .00125, .001375, .0015]#[.001, .00125, .0015, .00175, .002]
stop = [.000025, .00005, .000075, .0001]#[.0001, .00015, .0002, .00022, .00025, .0003]

for i in start:
    for j in stop:
        bslip = []
        step = (j - i)/57
        temp = i
        for k in range(58):
            bslip.append(temp)
            temp += step
        run1 = basic_model.isothermalISM(58, 1000, bslip, b0[:])
        for k in range(1500): #5000 years
            run1.timestep(1)
            #if(k%100==0): 
                #print 'on timestep', k
        print 'for start', i, 'and stop', j,'surface difference is', tools.calculate_surface_difference(run1.get_surface_elev() ,obs_surf)

#first experiment gives lowest difference for start .00125 and stop .0001, updating start and stop again reflecting this
