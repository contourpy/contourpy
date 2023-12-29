#ifndef CONTOURPY_CONTOUR_GENERATOR_H
#define CONTOURPY_CONTOUR_GENERATOR_H

#include "common.h"

namespace contourpy {

class ContourGenerator
{
public:
    // Non-copyable and non-moveable.
    ContourGenerator(const ContourGenerator& other) = delete;
    ContourGenerator(const ContourGenerator&& other) = delete;
    ContourGenerator& operator=(const ContourGenerator& other) = delete;
    ContourGenerator& operator=(const ContourGenerator&& other) = delete;

    virtual ~ContourGenerator() = default;

    virtual py::tuple filled(double lower_level, double upper_level) = 0;

    virtual py::sequence lines(double level) = 0;

protected:
    ContourGenerator() = default;
};

} // namespace contourpy

#endif // CONTOURPY_CONTOUR_GENERATOR_H
