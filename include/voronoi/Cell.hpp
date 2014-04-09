#pragma once

namespace voronoi
{
  /// Data structure for a single voronoi cell
  struct Cell
  {
    Cell() {}
    Cell(std::string const& _str) 
    {
      fromStr(_str);
    }
  
    float posx_, posy_;
    float weightx_, weighty_;
    float r_,g_,b_,a_;

    /// Voronoi from string
    void fromStr(std::string const& _str)
    {
      std::istringstream _is(_str);
      _is >> posX_ >> posY_ >> weightX_ >> weightY_;
      _is >> r_ >> g_ >> b_ >> a_;
    }
  };
}

