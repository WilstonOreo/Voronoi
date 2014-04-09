#define HALFDOME
//#define FULLDOME

#include "projector.h"

#ifdef FULLDOME
#include "fulldome.h"
#endif

#ifdef HALFDOME
#include "halfdome.h"
#endif

float canvas_params(in vec2 screenCoord)
{
  proj_params();
  canvas_params();

  if (canvas_intersection(proj_frustum_ray(screenCoord),canvas.iPoint) < 0.0)
  {
    return -1.0;
  }
  
  canvas.normal = canvas_normal();
  return 1.0;
}

