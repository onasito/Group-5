/*
*  Name: Joel Mendoza
*/

#include <iostream>
#include <iomanip>
#include <cmath>

int main() {
    // Variable declaration
    double x1, y1, x2, y2;
    
    // Input phase
    std::cin >> x1 >> y1 >> x2 >> y2;
    std::cout << std::endl;

    // Compute differences
    double dx = x2 - x1;
    double dy = y2 - y1;
    
    // Compute segment length
    double segment_length = std::hypot(dx, dy);

    // Determine line equation and slope
    std::string slope_direction;
    double slope = 0.0;
    double y_intercept = 0.0;
    
    if (dx == 0) {  // Vertical line case
        slope_direction = "vertical";
    } else {
        slope = dy / dx;
        y_intercept = y1 - (slope * x1);

        if (slope > 0) {
            slope_direction = "increasing";
        } else if (slope < 0) {
            slope_direction = "decreasing";
        } else {
            slope_direction = "horizontal";
        }
    }

    // Output phase
    std::cout << std::fixed << std::setprecision(2);
    std::cout << "Line equation:       ";
    if (dx == 0) {
        std::cout << "x = " << x1 << std::endl;
    } else {
        std::cout << "y = " << slope << "x + " << y_intercept << std::endl;
    }
    std::cout << "Slope direction:     " << slope_direction << std::endl;
    std::cout << "Line segment length: " << segment_length << std::endl;
    std::cout << "Slope:               " << slope << std::endl;

    return 0;
}
