target(
  name='targets',
  dependencies=[
    ':stackage_package',
    ':hackage_package',
    ':local_package',
  ]
)

python_library(
  name='stackage_package',
  sources=[
    'stackage_package.py',
  ],
  dependencies=[
    ':haskell_package',
  ]
)

python_library(
  name='hackage_package',
  sources=[
    'hackage_package.py',
  ],
  dependencies=[
    ':haskell_package',
  ]
)

python_library(
  name='local_package',
  sources=[
    'local_package.py',
  ],
  dependencies=[
    ':haskell_package',
  ]
)

python_library(
  name='haskell_package',
  sources=[
    'haskell_package.py',
  ],
  dependencies=[
    'src/python/pants/base:target'
  ],
)
