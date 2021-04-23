#include "line.h"
#include <cmath>


std::vector<Point> draw_line_DDA(Point p_src, Point p_dst) {

	std::vector<Point> result;
	float x0 = p_src.x, y0 = p_src.y;
	float x1 = p_dst.x, y1 = p_dst.y;
	float dx = x1 - x0;
	float dy = y1 - y0;
	int steps = abs(y1 - y0);
	if (fabs(dx)>fabs(dy))
		steps = abs(x1 - x0);
	//初始化
	float x = x0;
	float y = y0;
	//增量
	float xinc = dx / steps;
	float yinc = dy / steps;
	Point po;
	po.x = round(x); po.y = round(y);
	result.push_back(po);
	for (int i = 0; i<steps; ++i)
	{
		x += xinc;
		y += yinc;

		po.x = round(x); po.y = round(y);
		result.push_back(po);
	}
	return result;
}


std::vector<Point> draw_line_bresenham(Point p_src, Point p_dst) {
  

	std::vector<Point> result;
	int x0 = p_src.x, y0 = p_src.y, x1 = p_dst.x, y1 = p_dst.y;
	int dx = abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
	int dy = abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    int err = (dx > dy ? dx : -dy) / 2, e2;
	for (;;) {
		Point P;
		P.x = x0;
		P.y = y0;
		if (x0 == x1 && y0 == y1) break;
		e2 = err;
		if (e2 > -dx) { err -= dy; x0 += sx; }
		if (e2 < dy) { err += dx; y0 += sy; }
	}

  return result;
}
