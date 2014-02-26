import sys
import re
import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# took from https://raw.github.com/cburgmer/pdfserver/master/setup.py
def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements


def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def get_content(fname):
    dot = os.path.dirname(os.path.abspath(__file__))
    fpath = os.path.join(dot, fname)
    with open(fpath) as f:
        return f.read()


setup(name='keyhub',
      version='0.1dev',
      description='A repository for public ssh keys',
      long_description=get_content('README.md'),
      author='Felipe Reyes',
      author_email='freyes@tty.cl',
      url='http://keyhub.tty.cl',
      license='Apache License v2.0',
      packages=find_packages(),
      install_requires=parse_requirements('requirements.txt'),
      dependency_links=parse_dependency_links('requirements.txt'),
      test_requires=parse_requirements('test-requirements.txt'),
      cmdclass = {'test': Tox},
      include_package_data=True,
      zip_safe=False,
      entry_points={
          'console_scripts': [
              'keyhub = keyhub.app:main'
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
      ],
     )
