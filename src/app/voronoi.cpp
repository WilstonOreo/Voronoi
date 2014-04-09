#include <boost/program_options.hpp>

#include "MainWindow.h"
#include <QApplication>
#include <QFile>
#include <QGLFormat>

#include <voronoi/DataProvider.h>

using namespace std;
using namespace idm;

namespace po = boost::program_options;

int main(int ac, char* av[])
{
  QGLFormat f;
  f.setDoubleBuffer(false);
  f.setVersion(3,3);
  QGLFormat::setDefaultFormat(f);

  stringstream descStr;
  descStr << "Allowed options";

  // Declare the supported options
  po::options_description desc(descStr.str());

  desc.add_options()
  ("help,h", "Display help message.")
  ("input,i", po::value<string>(&_input), "Data input file")
  ;
  // Parse the command line arguments for all supported options
  po::variables_map vm;
  po::store(po::parse_command_line(ac, av, desc), vm);
  po::notify(vm);

  if (vm.count("help"))
  {
    cout << desc << endl;
    return EXIT_FAILURE;
  }

  /// Start gui
  QApplication _a(ac, av);

  voronoi::DataProvider _dataProvider(_input);
  MainWindow _w;
  _w.parametersFrame->setLayout(new tbd::ParameterForm(&_dataProvider));
  _w.connect(
      parametersFrame->layout(),SIGNAL(valueChanged()),
      &_w,SLOT(updateParameters()));

  _w.setWindowState(Qt::WindowMaximized);

  return _a.exec();
}
