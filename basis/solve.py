#!/usr/local/bin/python
from basis import msg
def examples():
    """Prints examples of using the script to the console using colored output.
    """
    script = "BASIS: 1D Solver for QM problems"
    explain = ("For 1D potentials such as square wells (infinite and finite), harmonic"
               "oscillator, Kronig-Penney, etc.")
    contents = [(("Solve the potential in `kp.cfg` using 200 basis functions"), 
                 "solve.py 200 -potential kp.cfg",
                 "This saves the solution to the default 'output.dat' "
                 "file in the current directory."),
                (("Solve the potential in `kp.cfg` and plot the solution."),
                 "solve.py 200 -potential kp.cfg -plot",""),
                (("Solve the potential `sho.cfg`, save the solution to `mysol.out`."),
                 "solve.py 400 -potential sho.cfg -outfile mysol.out","")]
    required = ("REQUIRED: potential config file `pot.cfg`")
    output = ("RETURNS: plot window; for logging-only mode, the data being "
              "logged is also periodically printed to stdout.")
    details = ("The plotting uses `matplotlib` with the default-configured "
               "backend. If you want a different backend, set the rc config "
               "for `matplotlib` using online documentation. ")
    outputfmt = ("")

    msg.example(script, explain, contents, required, output, outputfmt, details)

script_options = {
    "N": dict(default="100", type=int,
              help=("Specifies the number of basis functis to use "
                    "in the expansion.")),
    "-plot": dict(action="store_true",
                  help =("Plots the solution")),
    "-potential": dict(help="Path to the file defining the potential parameters."),
    "-outfile": dict(default="output.dat",
                     help="Overide the default output file name.")
    }

def _parser_options():
    """Parses the options and arguments from the command line."""
    #We have two options: get some of the details from the config file,
    import argparse
    from basis import base
    pdescr = "1D Potential Quantum Solver"
    parser = argparse.ArgumentParser(parents=[base.bparser], description=pdescr)
    for arg, options in script_options.items():
        parser.add_argument(arg, **options)
        
    args = base.exhandler(examples, parser)
    if args is None:
        return

    return args

def run(args):
    print("RUNNING",args)
    return 0

if __name__ == '__main__': # pragma: no cover
    run(_parser_options())


