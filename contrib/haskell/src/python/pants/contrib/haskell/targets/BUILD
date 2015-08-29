target(
  name='targets',
  dependencies=[
    ':stackage_package',
  ]
)

python_library(
  name='haskell_package',
  source=['haskell_package.py'],
)

python_library(
  name='stackage_package',
  sources=['stackage_package.py'],
  dependencies=[
    ':haskell_package',
    'src/python/pants/base:target'
  ]
)
