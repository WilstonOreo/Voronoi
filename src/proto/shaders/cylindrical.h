#include "util.h"

struct Cylinder
{
  float radius;
  float height;
  vec3 center;
};

vec3 Cylinder_point(in Cylinder cyl, in vec2 texCoord)
{
  float phi = (texCoord.s - 0.5)* 2.0 * PI;
  return vec3(
    cyl.radius * sin(phi), 
    cyl.radius * cos(phi), 
    cyl.height * texCoord.t) + cyl.center;
}

vec2 Cylinder_texCoords(in Cylinder cyl, in vec3 iPoint)
{
  vec3 normal = iPoint - cyl.center;
  normal.z = 0.0;
  normal = normalize(normal);
  float s = fract(atan(normal.x,normal.y) / (2.0*PI) - 0.5);
  float t = fract((iPoint.z - cyl.center.z) / cyl.height);
  return vec2(s,t);  
}

float Cylinder_intersection(in Cylinder cyl, in Ray ray, out vec3 iPoint)
{
  vec3 o = ray.org - cyl.center;
  float a = dot(ray.dir.xy,ray.dir.xy);
  float b = 2.0 * dot(ray.dir.xy,ray.org.xy);
  float c = dot(ray.org.xy,ray.org.xy) - cyl.radius*cyl.radius;
  float t = solveQuadraticEquation(a,b,c);
  if (t < cyl.radius / 1000.0) return -1.0;

  iPoint = ray.org + t * ray.dir;
  if (iPoint.z > cyl.center.z || 
      iPoint.z < cyl.center.z - cyl.height) return -1.0;
  return 1.0;
}

