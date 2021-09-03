from conans import ConanFile, CMake, tools, Meson
import os


class GstpluginsbaseConan(ConanFile):
    name = "gst_plugins_base"
    version = "1.19.1"
    description = ""
    url = "https://github.com/GStreamer/gst-plugins-base"
    homepage = "https://github.com/GStreamer/gst-plugins-base"
    license = "GPLv2+"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {
        "shared": True
    }
    generators = "cmake", "pkg_config"
    requires = (
        "gstreamer/1.19.1",
        "gobject-introspection/1.68.0",
        "libffi/3.4.2",
    )
    source_subfolder = "gst-plugins-base"
    build_subfolder = "build"
    remotes = {'origin': 'https://github.com/GStreamer/gst-plugins-base.git'}

    def source(self):
        tools.mkdir(self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            self.run('git init')
            for key, val in self.remotes.items():
                self.run("git remote add %s %s" % (key, val))
            self.run('git fetch --all')
            self.run('git reset --hard %s' % (self.version))
            self.run('git submodule update --init --recursive')

    def build(self):
        tools.mkdir("install")
        install_path = os.getcwd() + "/install"
        with tools.chdir("../" + self.source_subfolder):
            self.run("meson setup ../build --prefix " + install_path)
        self.run("ninja")
        # meson = Meson(self)
        # meson.configure(build_folder=self.build_subfolder,
        #                 source_folder=self.source_subfolder)
        # meson.build()
        self.run("ninja install --verbose")
        for pc_file in os.listdir("install/lib/pkgconfig"):
            tools.replace_prefix_in_pc_file(
                f"install/lib/pkgconfig/{pc_file}", "${package_root_path_gst_plugins_base}")

    def package(self):
        self.copy("lib/*", "", "install")
        self.copy("include/*", "", "install")
        self.copy("bin/*", "", "install")
        self.copy("share/*", "", "install")

    def package_info(self):
        self.cpp_info.components['gst-plugins-base'].libs = tools.collect_libs(
            self)
        self.cpp_info.components['gst-plugins-base'].includedirs = [
            'include/gstreamer-1.0']
        self.cpp_info.components['gst-plugins-base'].requires = [
            'gstreamer::gstreamer-1.0', 'gobject-introspection::gobject-introspection', 'libffi::libffi']

        self.cpp_info.components['gstreamer-pbutils-1.0'].names['pkg_config'] = 'gstreamer-pbutils-1.0'
        self.cpp_info.components['gstreamer-pbutils-1.0'].names['cmake_find_package'] = 'gstreamer-pbutils-1.0'
        self.cpp_info.components['gstreamer-pbutils-1.0'].requires = [
            'gst-plugins-base', 'gstreamer::gstreamer-1.0']
        self.cpp_info.components['gstreamer-pbutils-1.0'].libs = ['gstpbutils-1.0']

        self.cpp_info.components['gstreamer-audio-1.0'].names['pkg_config'] = 'gstreamer-audio-1.0'
        self.cpp_info.components['gstreamer-audio-1.0'].names['cmake_find_package'] = 'gstreamer-audio-1.0'
        self.cpp_info.components['gstreamer-audio-1.0'].requires = [
            'gst-plugins-base', 'gstreamer::gstreamer-1.0']
        self.cpp_info.components['gstreamer-audio-1.0'].libs = ['gstaudio-1.0']
        self.cpp_info.components['gstreamer-audio-1.0'].includedirs = [
            'include/gstreamer-1.0']
