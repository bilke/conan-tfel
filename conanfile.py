import os
from conans import ConanFile, CMake, tools


class TfelConan(ConanFile):
    name = "tfel"
    version = "3.2.0"
    license = "MIT"
    author = "Lars Bilke, lars.bilke@ufz.de"
    url = "https://github.com/bilke/tfel"
    description = "MFront is a code generator which translates a set of closely related domain specific languages into plain C++ on top of the TFEL library"
    topics = ("numerics", "mechanics", "materials")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        tools.get("https://github.com/thelfer/tfel/archive/TFEL-{0}.tar.gz"
                  .format(self.version))
        extracted_dir = self.name + "-" + self.name.upper() + "-" + self.version
        os.rename(extracted_dir, "tfel")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        if tools.os_info.is_macos:
            tools.replace_in_file("tfel/CMakeLists.txt", "set(PACKAGE_BUGREPORT \"tfel-contact@cea.fr\")",
                                  '''set(PACKAGE_BUGREPORT "tfel-contact@cea.fr")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

        # https://sourceforge.net/p/tfel/discussion/installation/thread/9a05c751cf
        tools.replace_in_file('tfel/src/System/SignalManager.cxx', '::sigfillset(&nSigSet);',
                              'sigfillset(&nSigSet);')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="tfel")
        cmake.build()
        # cmake.build(target='check')
        cmake.install()

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        # self.cpp_info.libs = ["tfel"]
        self.cpp_info.libs = tools.collect_libs(self)

