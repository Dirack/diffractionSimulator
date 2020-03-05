# diffraction-simulator
> Diffraction simulator scripts developed to the Madagascar seismic processing package

[Developed to Madagascar package, version 2.0.](http://www.ahay.org/wiki/Main_Page)

This package is a set of Madagascar SConstruct scripts to simulate several diffraction hyperbolas in a Stacked Section
and migrate with a velocity model that produce best focusing of the simulated hyperbolas.
After that simulation, it migrates the diffraction hyperbola, using local varimax focusing
measure and velocity continuation to get the migration velocity model and focalize the diffractions.

This script is based on the numerical experiment of the Madagascar reproducible paper
[Post-stack velocity analysis by separation and imaging of seismic diffractions](http://www.reproducibility.org/RSF/book/tccs/diffr/paper_html/)


## Development setup

You need to have the actual Madagascar package stable release installed on your computer. Please follow the
[Installing Madagascar page](http://www.ahay.org/wiki/Installation) in the official documentation.

## Installation

After Madagascar installing process, you need to install the programs of this repository in your local Madagascar user's
directory. You can compile and install it as any other Madagascar program. 
Usually, Madagascar keeps the path of your local copy source files in the $RSFSRC environment variable. You can
show that on a bash terminal using 'echo' command:

```sh
~$ echo "$RSFSRC"
```

And Madagascar will install executable files on your $RSFROOT directory. You can show that environment variable
with 'echo' too:

```sh
~$ echo "$RSFROOT"
```

Madagascar stores user programs in $RSFSRC/user directory. So, you can create a new directory or put this
repository inside that directory. In this repository, such as every user's repository in Madagascar, we have a compilation 
[SConstruct](https://github.com/Dirack/vfsa/blob/master/SConstruct) that compile the C programs.
Run 'scons' on your $RSFSRC/user/vfsa repository to compile it:

```shell
~$ scons
```

And run 'scons install' in the top directory of your local Madagascar installation 
(the directory path in your $RSFSRC variable):

```shell
~$ sudo scons install
```

If you have any doubt about this process, please reffer to the oficial documentation in 
[Adding_new_programs_to_Madagascar](http://www.ahay.org/wiki/Adding_new_programs_to_Madagascar)

## Usage example

A few motivating and useful examples of how that product can be used. 
_For examples and usage, please refer to the [Wiki](https://github.com/Dirack/diffractionSimulator/wiki)._

We also have many SConstruct examples in this repository in the
[experiments directory](https://github.com/Dirack/diffractionSimulator/tree/study/0.1/study)

## Release History
   
* [v1.0-beta.1](https://github.com/Dirack/diffractionSimulator/releases/tag/v1.0) - Work in progress
  * Beta version.
  
## Meta

Rodolfo Dirack – [@dirack](https://github.com/Dirack) – rodolfo_profissional@hotmail.com

Distributed under the GPL3 license. See ``LICENSE`` for more information.

[cre-gather-interpolation main page](https://github.com/Dirack/diffractionSimulator)

## Contributing

1. Fork it (<https://github.com/Dirack/diffractionSimulator/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

#### Important: The commit history should be clear, with commit mesages around one or two paraghraps describing your modifications. Pull Requests with unsatisfactory commit history will be rejected.
