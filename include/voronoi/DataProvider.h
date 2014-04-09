#pragma once

#include <tbd/serialize.h>
#include "Cell.hpp"

namespace voronoi
{
  /// Provides all cell data and parameters used by the voronoi 
  class DataProvider : 
    public Serializer<DataProvider>
  {
    TBD_PARAMETER_LIST
    (
       (float) weight_min,
       (float) weight_max,
       (float) radius_max,
       (float) cone_shape, // (from -12 to 12) (minus=log-like / positive=exp-like)
       (float) transition_zone_size,
       (Color4) transition_zon_color,
       (float) gradient,
       (Color4) gradient_color
    )
  public:
    DataProvider(std::string const& _filename) : 
      weight_min_(0),
      weight_max_(1),
      radius_max_(10),
      coneshape_(0),
      transition_zone_size_(0),
      transition_zone_color_(0,0,0,0),
      gradient_(0),
      gradient_color_(0)
    {
      loadData(_filename);
    }

    /// Loads cell from a ASCII string list file
    inline void loadData(std::string const& _filename)
    {
      cells_.clear();
      std::ifstream _fs(_filename);
      for (std::string _line; _fs.good(); _line = std::get_line(_fs))
      {
        cells_.emplace_back(_line);
      }
    }

    /// These parameters are needed to generate the widgets
    void additionalParameters(tbd::Config& _cfg)
    {
      using tbd::parameter;

      make(_cfg,"weight_min","slider",
      {
        {"type","slider"},
        {"min","0.0"},
        {"max","1.0"}
      });
      
      make(_cfg,"weight_max","slider",
      {
        {"type","slider"},
        {"min","0.0"},
        {"max","1.0"}
      });
      
      make(_cfg,"radius_max","slider",
      {
        {"type","slider"},
        {"min","0.0"},
        {"max","1.0"}
      });
      
      make(_cfg,"cone_shape","slider",
      {
        {"type","slider"},
        {"min","0.0"},
        {"max","1.0"}
      });
    }

    TBD_PROPERTY_REF(std::vector<Cell>,cells)
  };
}
