from conans import ConanFile, CMake, tools
import os


class PahomqttcConan(ConanFile):
    name = "libpaho-mqtt-c"
    version = "1.0.0"
    license = "EDL/EPL"
    description = "Paho MQTT client library"
    url = "https://github.com/geotracsystems/paho.mqtt.c"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "static": [True, False],
        "enable_ssl": [True, False],
        "build_documentation": [True, False],
        "build_samples": [True, False],
    }
    default_options = ("static=True", "enable_ssl=False",
                       "build_documentation=False", "build_samples=False")
    generators = "cmake"
    exports_sources = "*"

    def build(self):
        cmake = CMake(self)
        static = "-DPAHO_BUILD_STATIC=TRUE" if self.options.static else ""
        enable_ssl = "-DPAHO_WITH_SSL=TRUE" if self.options.enable_ssl else ""
        build_documentation = "-DPAHO_BUILD_DOCUMENTATION=TRUE" if self.options.build_documentation else ""
        build_samples = "-DPAHO_BUILD_SAMPLES=TRUE" if self.options.build_samples else ""
        # Set our install prefix, we don't really need to copy files with some packages
        #install_dir = "-DCMAKE_INSTALL_PREFIX=%s" % self.package_folder
        if self.settings.arch == "x86":
            os.environ["CFLAGS"] = "-m32"
        self.run('cmake ./ %s %s %s %s %s' % (cmake.command_line, static,
                                                 enable_ssl, build_documentation,
                                                 build_samples))
        self.run("cmake --build . %s" % cmake.build_config)
        #self.run("make install")

    def package(self):
        self.copy("MQTTAsync.h", dst="include", src="src")
        self.copy("MQTTClient.h", dst="include", src="src")
        self.copy("MQTTClientPersistence.h", dst="include", src="src")
        if(self.options.static):
            self.copy("*.a", dst="lib", src="src")
        else:
            self.copy("*.so", dst="lib", src="src")

    def package_info(self):
        if(self.options.static):
            self.cpp_info.libs = ["paho-mqtt3a-static", "paho-mqtt3c-static"]
        else:
            self.cpp_info.libs = ["paho-mqtt3a", "paho-mqtt3c"]
