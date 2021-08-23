# Allow user to directly use vloginit without installing it
import os
import sys
sys.path.append(os.path.dirname("./"))

import vloginit.main
vloginit.main.main()
