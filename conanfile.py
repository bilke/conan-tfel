import os
from conans import ConanFile, CMake, tools


class TfelConan(ConanFile):
    name = "tfel"
    version = "3.3.0"
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
        #tools.get("https://github.com/thelfer/tfel/archive/TFEL-{0}.tar.gz"
        #          .format(self.version))
        #extracted_dir = self.name + "-" + self.name.upper() + "-" + self.version
        # TODO: temp. fix for gcc 10 issues
        tools.get("https://github.com/thelfer/tfel/archive/rliv-3.3.zip")
        extracted_dir = "tfel-rliv-3.3"
        os.rename(extracted_dir, "tfel")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        if tools.os_info.is_macos:
            tools.replace_in_file("tfel/CMakeLists.txt", "set(PACKAGE_BUGREPORT \"tfel-contact@cea.fr\")",
                                  '''set(PACKAGE_BUGREPORT "tfel-contact@cea.fr")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(KEEP_RPATHS)
''')
            tools.replace_in_file("tfel/CMakeLists.txt", "set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)",
                "set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)")
            tools.replace_in_file("tfel/CMakeLists.txt", "set(CMAKE_INSTALL_RPATH \"${CMAKE_INSTALL_PREFIX}/lib\")",
                "set(CMAKE_INSTALL_RPATH \"@executable_path/../lib\")")


        # https://sourceforge.net/p/tfel/discussion/installation/thread/9a05c751cf
        tools.replace_in_file('tfel/src/System/SignalManager.cxx', '::sigfillset(&nSigSet);',
                              'sigfillset(&nSigSet);')

    def configure_cmake(self):
        cmake = CMake(self)
        cmake.configure(source_folder="tfel")
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

