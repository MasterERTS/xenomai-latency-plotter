import sys, os
import optparse
import matplotlib.pyplot as plt

def process_cmd():
    parser = optparse.OptionParser(description="Plot the result of cyclictest")
    parser.add_option("-f", "--file", dest='result_file', default="")
    opts, args = parser.parse_args()
    if not os.path.exists(opts.result_file):
        parser.print_help()
        sys.exit(-1)
    return os.path.realpath(opts.result_file)

def process_output(result_file):
    with open(result_file) as f:
        try:
            found_hist = False
            hist_data = {}
            lat_count = 0
            max_lat = []
            min_lat = []
            avg_lat = []
            for line in f.readlines():
                if line.strip().lower() == "# histogram":
                    found_hist = True
                    continue
                if line.strip().lower().startswith("# total:"):
                    found_hist = False
                    continue
                if found_hist:
                    temp_data = line.strip().split()
                    cpu_num = len(temp_data) - 1
                    lat_value = int(temp_data[0])
                    for x in range(1, cpu_num + 1):
                        lat_count = int(temp_data[x])
                        if lat_count != 0:
                            if x not in hist_data:
                                hist_data[x] = []
                            hist_data[x].append((lat_value, lat_count))
                if line.strip().lower().startswith("# min latencies"):
                    min_lat = [int(item) for item in (line.split(":")[1].split())]
                if line.strip().lower().startswith("# avg latencies"):
                    avg_lat = [int(item) for item in (line.split(":")[1].split())]
                if line.strip().lower().startswith("# max latencies"):
                    max_lat = [int(item) for item in (line.split(":")[1].split())]
        except FileNotFoundError:
            print("File not found !!")
            exit()

    return hist_data, min_lat, max_lat, avg_lat

def draw_figure(hist_data, min, max, avg):
    color_table=['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    cpu_count = 0
    lat_avg = 0
    plt.style.use('ggplot')
    lat_max = 0
    lat_min = 0
    for cpu_no in hist_data.keys():
        x = [item[0] for item in hist_data[cpu_no]]
        y = [item[1] for item in hist_data[cpu_no]]
        stddev = 0
        samples = 0
        variant = 0
        for index in range(0, len(x) -1):
            #print x[index], avg[cpu_no-1], y[index]
            variant += (x[index] - avg[cpu_no-1]) * (x[index] - avg[cpu_no-1]) * y[index]
            samples += y[index]
        variant = variant/samples
        #print variant, samples
        stddev = variant**(.5)
        fig = plt.plot(x, y, "-"+color_table[cpu_no - 1]+'*',
                       label="cpu[%s]:avg=%d,min=%d,max=%d,std=%f" % (cpu_no, avg[cpu_no-1], min[cpu_no-1], max[cpu_no-1], stddev))
        lat_avg += avg[cpu_no-1]
        if lat_min == 0:
            lat_min = min[cpu_no-1]
        if lat_max < max[cpu_no-1]:
            lat_max = max[cpu_no-1]
        cpu_count += 1

    plt.legend()
    plt.ylabel("Number of Samples")
    plt.xlabel("Latency (us): avg=%d, min=%d, max=%d" % (lat_avg/cpu_count, lat_min, lat_max))
    plt.savefig('../figs/last_fig_cycl.png')
    plt.show()

if __name__ == "__main__":
    #process_output(sys.argv[1])
    hist, min, max, avg = process_output(process_cmd())
    draw_figure(hist, min, max, avg)
