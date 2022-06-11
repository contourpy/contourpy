import numpy as np
from numpy.testing import assert_allclose
import pytest

from contourpy import LineType, ZInterp, contour_generator


@pytest.fixture
def xyz_log():
    n = 4
    angle = 0.4
    x, y = np.meshgrid(np.linspace(0.0, 1.0, n), np.linspace(0.0, 1.0, n))

    # Rotate grid
    rot = [[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]]
    x, y = np.einsum("ji,mni->jmn", rot, np.dstack([x, y]))

    z = 10.0**(2.5*y)
    return x, y, z


@pytest.mark.parametrize("name", ["serial", "threaded"])
@pytest.mark.parametrize("quad_as_tri", [False, True])
def test_z_interp_log(xyz_log, name, quad_as_tri):
    x, y, z = xyz_log
    cont_gen = contour_generator(
        x, y, z, name=name, z_interp=ZInterp.Log, line_type=LineType.Separate,
        quad_as_tri=quad_as_tri)
    levels = [0.3, 1, 3, 10, 30, 100]
    all_lines = []
    for level in levels:
        expected_y = np.log10(level) / 2.5
        lines = cont_gen.lines(level)
        assert len(lines) == 1
        line_y = lines[0][:, 1]
        assert_allclose(line_y, expected_y, atol=1e-15)
        all_lines.append(lines)
    # The following should all produce the same lines:
    #   contour_generator(...,       z , z_interp=ZInterp.Log   ).lines(      level )
    #   contour_generator(...,   log(z), z_interp=ZInterp.Linear).lines(  log(level))
    #   contour_generator(...,  log2(z), z_interp=ZInterp.Linear).lines( log2(level))
    #   contour_generator(..., log10(z), z_interp=ZInterp.Linear).lines(log10(level))
    for func in (np.log, np.log2, np.log10):
        cont_gen = contour_generator(
            x, y, func(z), name=name, z_interp=ZInterp.Linear, line_type=LineType.Separate,
            quad_as_tri=quad_as_tri)
        for i, level in enumerate(levels):
            lines = cont_gen.lines(func(level))
            assert len(lines) == 1
            assert_allclose(lines[0], all_lines[i][0], atol=1e-15)


@pytest.mark.parametrize("name", ["serial", "threaded"])
def test_z_interp_log_saddle(name):
    x = y = np.asarray([-1.0, 1.0])
    z = np.asarray([[1.0, 100.0], [100.0, 1.0]])
    # z at middle of saddle quad is 10.0 for log interpolation.  Contour lines above z=10 should
    # rotate clockwise around the middle, contour lines below z=10 rotate anticlockwise.
    cont_gen = contour_generator(
        x, y, z, name=name, z_interp=ZInterp.Log, line_type=LineType.Separate)
    for level in [1.1, 9.9, 10.1, 99.9]:
        lines = cont_gen.lines(level)
        assert len(lines) == 2
        for line in lines:
            assert line.shape == (2, 2)
            cross_product = np.cross(line[0], line[1])
            if level > 10.0:
                assert cross_product < 0.0
            else:
                assert cross_product > 0.0


@pytest.mark.parametrize("name", ["serial", "threaded"])
def test_z_interp_negative(name):
    msg = "z values must be positive if using ZInterp.Log"

    z = np.asarray([[1.0, 2.0], [3.0, 4.0]])
    for value in (0.0, -1.2):
        z[1, 1] = value
        with pytest.raises(ValueError, match=msg):
            _ = contour_generator(z=z, name=name, z_interp=ZInterp.Log)

    # Mask out negative value so no exception.
    z = np.ma.masked_less_equal(z, 0.0)
    _ = contour_generator(z=z, name=name, z_interp=ZInterp.Log)
