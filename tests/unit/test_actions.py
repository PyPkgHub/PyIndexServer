
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../.github')))
from actions import main as github_action

def execute_main(pkg_name, versions, short_desc, homepage):
    # Delete
    
    
    # Register
    os.environ['PKG_ACTION'] = 'REGISTER'
    os.environ['PKG_NAME'] = pkg_name
    os.environ['PKG_VERSION'] = versions[0]
    os.environ['PKG_AUTHOR'] = 'Nicolas Remond'
    os.environ['PKG_SHORT_DESC'] = short_desc
    os.environ['PKG_HOMEPAGE'] = homepage
    github_action()
    print(f'Package {pkg_name} registered')
    
    # Update
    for version in versions[1:]:
        os.environ['PKG_ACTION'] = 'UPDATE'
        os.environ['PKG_NAME'] = pkg_name
        os.environ['PKG_VERSION'] = version
        github_action()
        print(f'Package {pkg_name} updated to version {version}')
    print(f'Package {pkg_name} done')

def test_action_delete():
    os.environ['PKG_ACTION'] = 'DELETE'
    os.environ['PKG_NAME'] = 'testpkg'
    github_action()
    
    print(f'Package testpkg deleted')

def test_action_register():
    os.environ['PKG_ACTION'] = 'REGISTER'
    os.environ['PKG_NAME'] = 'testpkg'
    os.environ['PKG_VERSION'] = '1.1.1'
    os.environ['PKG_AUTHOR'] = 'Unknown'
    os.environ['PKG_SHORT_DESC'] = 'test package fo Private Pypi - Python Package Index'
    os.environ['PKG_HOMEPAGE'] = 'https://github.com/haim-shulner/testpkg'
    github_action()

    print(f'Package testpkg registered')

def test_action_update():
    os.environ['PKG_ACTION'] = 'REGISTER'
    os.environ['PKG_NAME'] = 'testpkg'
    os.environ['PKG_VERSION'] = '1.1.2'
    os.environ['PKG_AUTHOR'] = 'Unknown'
    os.environ['PKG_SHORT_DESC'] = 'test package fo Private Pypi - Python Package Index'
    os.environ['PKG_HOMEPAGE'] = 'https://github.com/haim-shulner/testpkg'
    github_action()

    print(f'Package testpkg updated')