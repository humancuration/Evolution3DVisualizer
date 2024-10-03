import cProfile
import pstats

def run_profiler():
    cProfile.run('import main_app; main_app.main()', 'profile_stats.prof')

def print_profiler_stats():
    p = pstats.Stats('profile_stats.prof')
    p.sort_stats('cumulative').print_stats(20)

if __name__ == "__main__":
    run_profiler()
    print_profiler_stats()