#include "util.h"

#ifdef MAP_DYNAMIC
uniform int map_mode;
#endif

#ifdef MAP_FISHEYE
// Get fisheye camera ray from screen coordinates 
float fisheye_direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
	vec2 uv = screenCoord.xy / res;
	uv = uv - 0.5;
  float phi = atan(uv.x,uv.y);
  float l = length(uv);
  
  if (l > 0.5)
  {
    return -1.0;
  }
  float theta  = l * PI;
  rd = normalize(vec3(sin(theta)*cos(phi),sin(theta)*sin(phi),cos(theta)));
  return 1.0;
}
#endif

#ifdef MAP_SPHERICAL
float spherical_direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
	vec2 uv = screenCoord.xy / res;
  float theta = (uv.t) * PI,
        phi = (uv.s - 0.5)* 2.0 * PI;
  rd = vec3(sin(theta) * sin(phi), sin(theta) * cos(phi), cos(theta));
  return 1.0;
}
#endif
#ifdef MAP_CUBE
float cubemap_direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
	vec2 uv = screenCoord.xy / res;
  uv.x *= 6.0;
  
  if (uv.x < 1.0) // EAST 
  {
    uv -= 0.5;
    rd = vec3(2.0*uv.x,1.0,-2.0*uv.y);
  } else
  if (uv.x < 2.0) // WEST
  {
    uv -= 0.5;
    uv.x -= 1.0;
    rd = vec3(-2.0*uv.x,-1.0,-2.0*uv.y);
  } else
  if (uv.x < 3.0) // NORTH
  {
    uv -= 0.5;
    uv.x -= 2.0;
    rd = vec3(1.0,-2.0*uv.xy);
  } else
  if (uv.x < 4.0) // SOUTH
  {
    uv -= 0.5;
    uv.x -= 3.0;
    rd = vec3(-1.0,2.0*uv.x,-uv.y*2.0);
  } else
  if (uv.x < 5.0) // Top
  {
    uv -= 0.5;
    uv.x -= 4.0;
    rd = vec3(2.0*uv,1.0);
  } else
  if (uv.x < 6.0) // Bottom
  {
    uv -= 0.5;
    uv.x -= 5.0;
    rd = vec3(-uv.x*2.0,uv.y*2.0,-1.0);
  }

  rd = normalize(rd);

  return 1.0;
}
#endif 
#ifdef MAP_DYNAMIC
float direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
#ifdef MAP_SPHERICAL
  if (map_mode == MAP_SPHERICAL)
  {
    return spherical_direction(screenCoord,res,rd);
  }
#endif
#ifdef MAP_FISHEYE
  if (map_mode == MAP_FISHEYE)
  {
    return fisheye_direction(screenCoord,res,rd);
  }
#endif 
#ifdef MAP_CUBE
  if (map_mode == MAP_CUBE)
  {
    return cubemap_direction(screenCoord,res,rd);
  }
#endif
  return -1.0;
}

#endif

#ifndef MAP_DYNAMIC
#ifdef MAP_SPHERICAL
float direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
  return spherical_direction(screenCoord,res,rd);
}
#endif 
#ifdef MAP_FISHEYE
float direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
  return fisheye_direction(screenCoord,res,rd);
}
#endif 
#ifdef MAP_CUBE
float direction(in vec2 screenCoord, in vec2 res, out vec3 rd)
{
  return cubemap_direction(screenCoord,res,rd);
}
#endif 
#endif




// Get fisheye camera ray from screen coordinates with rotation
float direction(in vec2 screenCoord, in vec2 res, float rotX, float rotY, float rotZ, out vec3 rd)
{
  if (direction(screenCoord,res,rd) < 0.0)
  {
    return -1.0;
  }
  rd *= rotateAroundZ(rotZ)*rotateAroundY(rotY)*rotateAroundX(rotX);
  return 1.0;
}



