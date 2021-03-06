# coding: utf-8
"""
    weasyprint.tests.tables
    -----------------------

    Tests for layout of tables.

    :copyright: Copyright 2011-2016 Simon Sapin and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

from __future__ import division, unicode_literals

from .test_boxes import render_pages as parse
from .test_draw import assert_pixels
from .testing_utils import assert_no_logs, capture_logs, requires


@assert_no_logs
def test_inline_table():
    """Test the inline-table elements sizes."""
    page, = parse('''
        <table style="display: inline-table; border-spacing: 10px;
                      margin: 5px">
            <tr>
                <td><img src=pattern.png style="width: 20px"></td>
                <td><img src=pattern.png style="width: 30px"></td>
            </tr>
        </table>
        foo
    ''')
    html, = page.children
    body, = html.children
    line, = body.children
    table_wrapper, text = line.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 0 + border-spacing
    assert td_1.width == 20
    assert td_2.position_x == 45  # 15 + 20 + border-spacing
    assert td_2.width == 30
    assert table.width == 80  # 20 + 30 + 3 * border-spacing
    assert table_wrapper.margin_width() == 90  # 80 + 2 * margin
    assert text.position_x == 90


@assert_no_logs
def test_implicit_width_table():
    """Test table with implicit width."""
    # See https://github.com/Kozea/WeasyPrint/issues/169
    page, = parse('''
        <table>
            <col style="width:25%"></col>
            <col></col>
            <tr>
                <td></td>
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children

    page, = parse('''
        <table>
            <tr>
                <td style="width:25%"></td>
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children


@assert_no_logs
def test_fixed_layout_table():
    """Test the fixed layout table elements sizes."""
    page, = parse('''
        <table style="table-layout: fixed; border-spacing: 10px;
                      margin: 5px">
            <colgroup>
              <col style="width: 20px" />
            </colgroup>
            <tr>
                <td></td>
                <td style="width: 40px">a</td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 5 + border-spacing
    assert td_1.width == 20
    assert td_2.position_x == 45  # 15 + 20 + border-spacing
    assert td_2.width == 40
    assert table.width == 90  # 20 + 40 + 3 * border-spacing

    page, = parse('''
        <table style="table-layout: fixed; border-spacing: 10px;
                      width: 200px; margin: 5px">
            <tr>
                <td style="width: 20px">a</td>
                <td style="width: 40px"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 5 + border-spacing
    assert td_1.width == 75  # 20 + ((200 - 20 - 40 - 3 * border-spacing) / 2)
    assert td_2.position_x == 100  # 15 + 75 + border-spacing
    assert td_2.width == 95  # 40 + ((200 - 20 - 40 - 3 * border-spacing) / 2)
    assert table.width == 200

    page, = parse('''
        <table style="table-layout: fixed; border-spacing: 10px;
                      width: 110px; margin: 5px">
            <tr>
                <td style="width: 40px">a</td>
                <td>b</td>
            </tr>
            <tr>
                <td style="width: 50px">a</td>
                <td style="width: 30px">b</td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row_1, row_2 = row_group.children
    td_1, td_2 = row_1.children
    td_3, td_4 = row_2.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 0 + border-spacing
    assert td_3.position_x == 15
    assert td_1.width == 40
    assert td_2.width == 40
    assert td_2.position_x == 65  # 15 + 40 + border-spacing
    assert td_4.position_x == 65
    assert td_3.width == 40
    assert td_4.width == 40
    assert table.width == 110  # 20 + 40 + 3 * border-spacing

    page, = parse('''
        <table style="table-layout: fixed; border-spacing: 0;
                      width: 100px; margin: 10px">
            <colgroup>
              <col />
              <col style="width: 20px" />
            </colgroup>
            <tr>
                <td></td>
                <td style="width: 40px">a</td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 10  # 0 + margin-left
    assert td_1.position_x == 10
    assert td_1.width == 80  # 100 - 20
    assert td_2.position_x == 90  # 10 + 80
    assert td_2.width == 20
    assert table.width == 100

    # With border-collapse
    page, = parse('''
        <style>
          /* Do not apply: */
          colgroup, col, tbody, tr, td { margin: 1000px }
        </style>
        <table style="table-layout: fixed;
                      border-collapse: collapse; border: 10px solid;
                      /* ignored with collapsed borders: */
                      border-spacing: 10000px; padding: 1000px">
            <colgroup>
              <col style="width: 30px" />
            </colgroup>
            <tbody>
              <tr>
                <td style="padding: 2px"></td>
                <td style="width: 34px; padding: 10px; border: 2px solid"></td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 0
    assert table.border_left_width == 5  # half of the collapsed 10px border
    assert td_1.position_x == 5  # border-spacing is ignored
    assert td_1.margin_width() == 30  # as <col>
    assert td_1.width == 20  # 30 - 5 (border-left) - 1 (border-right) - 2*2
    assert td_2.position_x == 35
    assert td_2.width == 34
    assert td_2.margin_width() == 60  # 34 + 2*10 + 5 + 1
    assert table.width == 90  # 30 + 60
    assert table.margin_width() == 100  # 90 + 2*5 (border)


@assert_no_logs
def test_auto_layout_table():
    """Test the auto layout table elements sizes."""
    page, = parse('''
        <body style="width: 100px">
        <table style="border-spacing: 10px; margin: auto">
            <tr>
                <td><img src=pattern.png></td>
                <td><img src=pattern.png></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table_wrapper.width == 38  # Same as table, see below
    assert table_wrapper.margin_left == 31  # 0 + margin-left = (100 - 38) / 2
    assert table_wrapper.margin_right == 31
    assert table.position_x == 31
    assert td_1.position_x == 41  # 31 + spacing
    assert td_1.width == 4
    assert td_2.position_x == 55  # 31 + 4 + spacing
    assert td_2.width == 4
    assert table.width == 38  # 3 * spacing + 2 * 4

    page, = parse('''
        <body style="width: 50px">
        <table style="border-spacing: 1px; margin: 10%">
            <tr>
                <td style="border: 3px solid black"><img src=pattern.png></td>
                <td style="border: 3px solid black">
                    <img src=pattern.png><img src=pattern.png>
                </td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 6  # 5 + border-spacing
    assert td_1.width == 4
    assert td_2.position_x == 17  # 6 + 4 + spacing + 2 * border
    assert td_2.width == 8
    assert table.width == 27  # 3 * spacing + 4 + 8 + 4 * border

    page, = parse('''
        <table style="border-spacing: 1px; margin: 5px; font-size: 0">
            <tr>
                <td></td>
                <td><img src=pattern.png><img src=pattern.png></td>
            </tr>
            <tr>
                <td>
                    <img src=pattern.png>
                    <img src=pattern.png>
                    <img src=pattern.png>
                </td>
                <td><img src=pattern.png></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row1, row2 = row_group.children
    td_11, td_12 = row1.children
    td_21, td_22 = row2.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_11.position_x == td_21.position_x == 6  # 5 + spacing
    assert td_11.width == td_21.width == 12
    assert td_12.position_x == td_22.position_x == 19  # 6 + 12 + spacing
    assert td_12.width == td_22.width == 8
    assert table.width == 23  # 3 * spacing + 12 + 8

    page, = parse('''
        <table style="border-spacing: 1px; margin: 5px">
            <tr>
                <td style="border: 1px solid black"><img src=pattern.png></td>
                <td style="border: 2px solid black; padding: 1px">
                    <img src=pattern.png>
                </td>
            </tr>
            <tr>
                <td style="border: 5px solid black"><img src=pattern.png></td>
                <td><img src=pattern.png></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row1, row2 = row_group.children
    td_11, td_12 = row1.children
    td_21, td_22 = row2.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_11.position_x == td_21.position_x == 6  # 5 + spacing
    assert td_11.width == 12  # 4 + 2 * 5 - 2 * 1
    assert td_21.width == 4
    assert td_12.position_x == td_22.position_x == 21  # 6 + 4 + 2 * b1 + sp
    assert td_12.width == 4
    assert td_22.width == 10  # 4 + 2 * 3
    assert table.width == 27  # 3 * spacing + 4 + 4 + 2 * b1 + 2 * b2

    page, = parse('''
        <style>
            @page { size: 100px 1000px; }
        </style>
        <table style="border-spacing: 1px; margin-right: 79px; font-size: 0">
            <tr>
                <td><img src=pattern.png></td>
                <td>
                    <img src=pattern.png> <img src=pattern.png>
                    <img src=pattern.png> <img src=pattern.png>
                    <img src=pattern.png> <img src=pattern.png>
                    <img src=pattern.png> <img src=pattern.png>
                    <img src=pattern.png>
                </td>
            </tr>
            <tr>
                <td></td>
            </tr>
        </table>
    ''')
    # Preferred minimum width is 2 * 4 + 3 * 1 = 11
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row1, row2 = row_group.children
    td_11, td_12 = row1.children
    td_21, = row2.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 0
    assert td_11.position_x == td_21.position_x == 1  # spacing
    assert td_11.width == td_21.width == 4  # minimum width
    assert td_12.position_x == 6  # 1 + 5 + sp
    assert td_12.width == 14  # available width
    assert table.width == 21

    page, = parse('''
        <table style="border-spacing: 10px; margin: 5px">
            <colgroup>
              <col style="width: 20px" />
            </colgroup>
            <tr>
                <td></td>
                <td style="width: 40px">a</td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 0 + border-spacing
    assert td_1.width == 20
    assert td_2.position_x == 45  # 15 + 20 + border-spacing
    assert td_2.width == 40
    assert table.width == 90  # 20 + 40 + 3 * border-spacing

    page, = parse('''
        <table style="border-spacing: 10px; width: 120px; margin: 5px;
                      font-size: 0">
            <tr>
                <td style="width: 20px"><img src=pattern.png></td>
                <td><img src=pattern.png style="width: 40px"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 5 + border-spacing
    assert td_1.width == 20  # fixed
    assert td_2.position_x == 45  # 15 + 20 + border-spacing
    assert td_2.width == 70  # 120 - 3 * border-spacing - 20
    assert table.width == 120

    page, = parse('''
        <table style="border-spacing: 10px; width: 110px; margin: 5px">
            <tr>
                <td style="width: 60px"></td>
                <td></td>
            </tr>
            <tr>
                <td style="width: 50px"></td>
                <td style="width: 30px"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row_1, row_2 = row_group.children
    td_1, td_2 = row_1.children
    td_3, td_4 = row_2.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 5  # 0 + margin-left
    assert td_1.position_x == 15  # 0 + border-spacing
    assert td_3.position_x == 15
    assert td_1.width == 60
    assert td_2.width == 30
    assert td_2.position_x == 85  # 15 + 60 + border-spacing
    assert td_4.position_x == 85
    assert td_3.width == 60
    assert td_4.width == 30
    assert table.width == 120  # 60 + 30 + 3 * border-spacing

    page, = parse('''
        <table style="border-spacing: 0; width: 14px; margin: 10px">
            <colgroup>
              <col />
              <col style="width: 6px" />
            </colgroup>
            <tr>
                <td><img src=pattern.png><img src=pattern.png></td>
                <td style="width: 8px"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 10  # 0 + margin-left
    assert td_1.position_x == 10
    assert td_1.width == 6  # 14 - 8
    assert td_2.position_x == 16  # 10 + 6
    assert td_2.width == 8  # maximum of the minimum widths for the column
    assert table.width == 14

    page, = parse('''
        <table style="border-spacing: 0">
            <tr>
                <td style="width: 10px"></td>
                <td colspan="3"></td>
            </tr>
            <tr>
                <td colspan="2" style="width: 22px"></td>
                <td style="width: 8px"></td>
                <td style="width: 8px"></td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td colspan="2"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row1, row2, row3 = row_group.children
    td_11, td_12 = row1.children
    td_21, td_22, td_23 = row2.children
    td_31, td_32, td_33 = row3.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 0
    assert td_11.width == 10  # fixed
    assert td_12.width == 28  # 38 - 10
    assert td_21.width == 22  # fixed
    assert td_22.width == 8  # fixed
    assert td_23.width == 8  # fixed
    assert td_31.width == 10  # same as first line
    assert td_32.width == 12  # 22 - 10
    assert td_33.width == 16  # 8 + 8 from second line
    assert table.width == 38

    page, = parse('''
        <table style="border-spacing: 10px">
            <tr>
                <td style="width: 10px"></td>
                <td colspan="3"></td>
            </tr>
            <tr>
                <td colspan="2" style="width: 32px"></td>
                <td style="width: 8px"></td>
                <td style="width: 8px"></td>
            </tr>
            <tr>
                <td></td>
                <td></td>
                <td colspan="2"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row1, row2, row3 = row_group.children
    td_11, td_12 = row1.children
    td_21, td_22, td_23 = row2.children
    td_31, td_32, td_33 = row3.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 0
    assert td_11.width == 10  # fixed
    assert td_12.width == 48  # 32 - 10 - sp + 2 * 8 + 2 * sp
    assert td_21.width == 32  # fixed
    assert td_22.width == 8  # fixed
    assert td_23.width == 8  # fixed
    assert td_31.width == 10  # same as first line
    assert td_32.width == 12  # 32 - 10 - sp
    assert td_33.width == 26  # 2 * 8 + sp
    assert table.width == 88

    # Regression tests: these used to crash
    page, = parse('''
        <table style="width: 30px">
            <tr>
                <td colspan=2></td>
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 20  # 2 / 3 * 30
    assert td_2.width == 10  # 1 / 3 * 30
    assert table.width == 30

    page, = parse('''
        <table style="width: 20px">
            <col />
            <col />
            <tr>
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, = row.children
    assert td_1.width == 20
    assert table.width == 20

    page, = parse('''
        <table style="width: 20px">
            <col />
            <col />
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    column_group, = table.column_groups
    column_1, column_2 = column_group.children
    assert column_1.width == 0
    assert column_2.width == 0

    # Absolute table
    page, = parse('''
        <table style="width: 30px; position: absolute">
            <tr>
                <td colspan=2></td>
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 20  # 2 / 3 * 30
    assert td_2.width == 10  # 1 / 3 * 30
    assert table.width == 30

    # With border-collapse
    page, = parse('''
        <style>
          /* Do not apply: */
          colgroup, col, tbody, tr, td { margin: 1000px }
        </style>
        <table style="border-collapse: collapse; border: 10px solid;
                      /* ignored with collapsed borders: */
                      border-spacing: 10000px; padding: 1000px">
            <colgroup>
              <col style="width: 30px" />
            </colgroup>
            <tbody>
              <tr>
                <td style="padding: 2px"></td>
                <td style="width: 34px; padding: 10px; border: 2px solid"></td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert table_wrapper.position_x == 0
    assert table.position_x == 0
    assert table.border_left_width == 5  # half of the collapsed 10px border
    assert td_1.position_x == 5  # border-spacing is ignored
    assert td_1.margin_width() == 30  # as <col>
    assert td_1.width == 20  # 30 - 5 (border-left) - 1 (border-right) - 2*2
    assert td_2.position_x == 35
    assert td_2.width == 34
    assert td_2.margin_width() == 60  # 34 + 2*10 + 5 + 1
    assert table.width == 90  # 30 + 60
    assert table.margin_width() == 100  # 90 + 2*5 (border)

    # Column widths as percentage
    page, = parse('''
        <table style="width: 200px">
            <colgroup>
              <col style="width: 70%" />
              <col style="width: 30%" />
            </colgroup>
            <tbody>
              <tr>
                <td>a</td>
                <td>abc</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 140
    assert td_2.width == 60
    assert table.width == 200

    # Column group width
    page, = parse('''
        <table style="width: 200px">
            <colgroup style="width: 100px">
              <col />
              <col />
            </colgroup>
            <col style="width: 100px" />
            <tbody>
              <tr>
                <td>a</td>
                <td>a</td>
                <td>abc</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3 = row.children
    assert td_1.width == 100
    assert td_2.width == 100
    assert td_3.width == 100
    assert table.width == 300

    # Multiple column width
    page, = parse('''
        <table style="width: 200px">
            <colgroup>
              <col style="width: 50px" />
              <col style="width: 30px" />
              <col />
            </colgroup>
            <tbody>
              <tr>
                <td>a</td>
                <td>a</td>
                <td>abc</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3 = row.children
    assert td_1.width == 50
    assert td_2.width == 30
    assert td_3.width == 120
    assert table.width == 200

    # Fixed-width table with column group with widths as percentages and pixels
    page, = parse('''
        <table style="width: 500px">
            <colgroup style="width: 100px">
              <col />
              <col />
            </colgroup>
            <colgroup style="width: 30%">
              <col />
              <col />
            </colgroup>
            <tbody>
              <tr>
                <td>a</td>
                <td>a</td>
                <td>abc</td>
                <td>abc</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3, td_4 = row.children
    assert td_1.width == 100
    assert td_2.width == 100
    assert td_3.width == 150
    assert td_4.width == 150
    assert table.width == 500

    # Auto-width table with column group with widths as percentages and pixels
    page, = parse('''
        <table>
            <colgroup style="width: 10%">
              <col />
              <col />
            </colgroup>
            <colgroup style="width: 200px">
              <col />
              <col />
            </colgroup>
            <tbody>
              <tr>
                <td>a a</td>
                <td>a b</td>
                <td>a c</td>
                <td>a d</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3, td_4 = row.children
    assert td_1.width == 50
    assert td_2.width == 50
    assert td_3.width == 200
    assert td_4.width == 200
    assert table.width == 500

    # Wrong column group width
    page, = parse('''
        <table style="width: 200px">
            <colgroup style="width: 20%">
              <col />
              <col />
            </colgroup>
            <tbody>
              <tr>
                <td>a</td>
                <td>a</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 100
    assert td_2.width == 100
    assert table.width == 200

    # Column width as percentage and cell width in pixels
    page, = parse('''
        <table style="width: 200px">
            <colgroup>
              <col style="width: 70%" />
              <col />
            </colgroup>
            <tbody>
              <tr>
                <td>a</td>
                <td style="width: 60px">abc</td>
              </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 140
    assert td_2.width == 60
    assert table.width == 200

    # Column width and cell width as percentage
    page, = parse('''
        <div style="width: 400px">
            <table style="width: 50%">
                <colgroup>
                    <col style="width: 70%" />
                    <col />
                </colgroup>
                <tbody>
                    <tr>
                        <td>a</td>
                        <td style="width: 30%">abc</td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 140
    assert td_2.width == 60
    assert table.width == 200

    # Test regression: https://github.com/Kozea/WeasyPrint/issues/307
    # Table with a cell larger than the table's max-width
    page, = parse('''
        <table style="max-width: 300px">
            <td style="width: 400px"></td>
        </table>
    ''')

    # Table with a cell larger than the table's width
    page, = parse('''
        <table style="width: 300px">
            <td style="width: 400px"></td>
        </table>
    ''')

    # Table with a cell larger than the table's width and max-width
    page, = parse('''
        <table style="width: 300px; max-width: 350px">
            <td style="width: 400px"></td>
        </table>
    ''')

    # Table with a cell larger than the table's width and max-width
    page, = parse('''
        <table style="width: 300px; max-width: 350px">
            <td style="padding: 50px">
                <div style="width: 300px"></div>
            </td>
        </table>
    ''')

    # Table with a cell larger than the table's max-width
    page, = parse('''
        <table style="max-width: 300px; margin: 100px">
            <td style="width: 400px"></td>
        </table>
    ''')

    # Test a table with column widths < table width < column width + spacing
    page, = parse('''
        <table style="width: 300px; border-spacing: 2px">
            <td style="width: 299px"></td>
        </table>
    ''')

    # Table with a cell larger than the table's width
    page, = parse('''
        <table style="width: 300px; margin: 100px">
            <td style="width: 400px"></td>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    assert table_wrapper.margin_width() == 600  # 400 + 2 * 100

    # Div with auto width containing a table with a min-width
    page, = parse('''
        <div style="float: left">
            <table style="min-width: 400px; margin: 100px">
                <td></td>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    assert div.margin_width() == 600  # 400 + 2 * 100
    assert table_wrapper.margin_width() == 600  # 400 + 2 * 100

    # Div with auto width containing an empty table with a min-width
    page, = parse('''
        <div style="float: left">
            <table style="min-width: 400px; margin: 100px"></table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    assert div.margin_width() == 600  # 400 + 2 * 100
    assert table_wrapper.margin_width() == 600  # 400 + 2 * 100

    # Div with auto width containing a table with a cell larger than the
    # table's max-width
    page, = parse('''
        <div style="float: left">
            <table style="max-width: 300px; margin: 100px">
                <td style="width: 400px"></td>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    assert div.margin_width() == 600  # 400 + 2 * 100
    assert table_wrapper.margin_width() == 600  # 400 + 2 * 100

    # Test regression on a crash: https://github.com/Kozea/WeasyPrint/pull/152
    page, = parse('''
        <table>
            <td style="width: 50%">
        </table>
    ''')

    # Other crashes: https://github.com/Kozea/WeasyPrint/issues/305
    page, = parse('''
        <table>
          <tr>
            <td>
              <table>
                <tr>
                  <th>Test</th>
                </tr>
                <tr>
                  <td style="min-width: 100%;"></td>
                  <td style="width: 48px;"></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
    ''')
    page, = parse('''
        <table>
          <tr>
            <td>
              <table>
                <tr>
                  <td style="width: 100%;"></td>
                  <td style="width: 48px;">
                    <img src="http://weasyprint.org/samples/acid2-small.png">
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
    ''')
    page, = parse('''
        <table>
          <tr>
            <td>
              <table style="display: inline-table">
                <tr>
                  <td style="width: 100%;"></td>
                  <td></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
    ''')

    # Test regression: https://github.com/Kozea/WeasyPrint/issues/368
    # Check that white-space is used for the shrink-to-fit algorithm
    page, = parse('''
        <table style="width: 0">
            <td style="font-family: ahem;
                       white-space: nowrap">a a</td>
        </table>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    assert table.width == 16 * 3

    # Cell width as percentage in auto-width table
    page, = parse('''
        <div style="width: 100px">
            <table>
                <tbody>
                    <tr>
                        <td>a a a a a a a a</td>
                        <td style="width: 30%">a a a a a a a a</td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 70
    assert td_2.width == 30
    assert table.width == 100

    # Cell width as percentage in auto-width table
    page, = parse('''
        <table>
            <tbody>
                <tr>
                    <td style="width: 70px">a a a a a a a a</td>
                    <td style="width: 30%">a a a a a a a a</td>
                </tr>
            </tbody>
        </table>
    ''')
    html, = page.children
    body, = html.children
    table_wrapper, = body.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2 = row.children
    assert td_1.width == 70
    assert td_2.width == 30
    assert table.width == 100

    # Cell width as percentage on colspan cell in auto-width table
    page, = parse('''
        <div style="width: 100px">
            <table>
                <tbody>
                    <tr>
                        <td>a a a a a a a a</td>
                        <td style="width: 30%" colspan=2>a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3 = row.children
    assert td_1.width == 35
    assert td_2.width == 30
    assert td_3.width == 35
    assert table.width == 100

    # Cells widths as percentages on normal and colspan cells
    page, = parse('''
        <div style="width: 100px">
            <table>
                <tbody>
                    <tr>
                        <td>a a a a a a a a</td>
                        <td style="width: 30%" colspan=2>a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                        <td style="width: 40%">a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td_1, td_2, td_3, td_4, td_5 = row.children
    assert td_1.width == 10
    assert td_2.width == 30
    assert td_3.width == 10
    assert td_4.width == 40
    assert td_5.width == 10
    assert table.width == 100

    # Cells widths as percentage on multiple lines
    page, = parse('''
        <div style="width: 1000px">
            <table>
                <tbody>
                    <tr>
                        <td>a a a a a a a a</td>
                        <td style="width: 30%">a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                        <td style="width: 40%">a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                    </tr>
                    <tr>
                        <td style="width: 31%" colspan=2>a a a a a a a a</td>
                        <td>a a a a a a a a</td>
                        <td style="width: 42%" colspan=2>a a a a a a a a</td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row_1, row_2 = row_group.children
    td_11, td_12, td_13, td_14, td_15 = row_1.children
    td_21, td_22, td_23 = row_2.children
    assert td_11.width == 10  # 31% - 30%
    assert td_12.width == 300  # 30%
    assert td_13.width == 270  # 1000 - 31% - 42%
    assert td_14.width == 400  # 40%
    assert td_15.width == 20  # 42% - 2%
    assert td_21.width == 310  # 31%
    assert td_22.width == 270  # 1000 - 31% - 42%
    assert td_23.width == 420  # 42%
    assert table.width == 1000

    # Test regression:
    # http://test.weasyprint.org/suite-css21/chapter8/section2/test56/
    page, = parse('''
        <div style="position: absolute">
            <table style="margin: 50px; border: 20px solid black">
                <tr>
                    <td style="width: 200px; height: 200px"></td>
                </tr>
            </table>
        </div>
    ''')
    html, = page.children
    body, = html.children
    div, = body.children
    table_wrapper, = div.children
    table, = table_wrapper.children
    row_group, = table.children
    row, = row_group.children
    td, = row.children
    assert td.width == 200
    assert table.width == 200
    assert div.width == 340  # 200 + 2 * 50 + 2 * 20


@assert_no_logs
def test_table_column_width():
    source = '''
        <style>
            body { width: 20000px; margin: 0 }
            table {
              width: 10000px; margin: 0 auto; border-spacing: 100px 0;
              table-layout: fixed
            }
            td { border: 10px solid; padding: 1px }
        </style>
        <table>
            <col style="width: 10%">
            <tr>
                <td style="width: 30%" colspan=3>
                <td>
            </tr>
            <tr>
                <td>
                <td>
                <td>
                <td>
            </tr>
            <tr>
                <td>
                <td colspan=12>This cell will be truncated to grid width
                <td>This cell will be removed as it is beyond the grid width
            </tr>
        </table>
    '''
    with capture_logs() as logs:
        page, = parse(source)
    assert len(logs) == 1
    assert logs[0].startswith('WARNING: This table row has more columns than '
                              'the table, ignored 1 cell')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    row_group, = table.children
    first_row, second_row, third_row = row_group.children
    cells = [first_row.children, second_row.children, third_row.children]
    assert len(first_row.children) == 2
    assert len(second_row.children) == 4
    # Third cell here is completly removed
    assert len(third_row.children) == 2

    assert body.position_x == 0
    assert wrapper.position_x == 0
    assert wrapper.margin_left == 5000
    assert wrapper.content_box_x() == 5000  # auto margin-left
    assert wrapper.width == 10000
    assert table.position_x == 5000
    assert table.width == 10000
    assert row_group.position_x == 5100  # 5000 + border_spacing
    assert row_group.width == 9800  # 10000 - 2*border-spacing
    assert first_row.position_x == row_group.position_x
    assert first_row.width == row_group.width

    # This cell has colspan=3
    assert cells[0][0].position_x == 5100  # 5000 + border-spacing
    # `width` on a cell sets the content width
    assert cells[0][0].width == 3000  # 30% of 10000px
    assert cells[0][0].border_width() == 3022  # 3000 + borders + padding

    # Second cell of the first line, but on the fourth and last column
    assert cells[0][1].position_x == 8222  # 5100 + 3022 + border-spacing
    assert cells[0][1].border_width() == 6678  # 10000 - 3022 - 3*100
    assert cells[0][1].width == 6656  # 6678 - borders - padding

    assert cells[1][0].position_x == 5100  # 5000 + border-spacing
    # `width` on a column sets the border width of cells
    assert cells[1][0].border_width() == 1000  # 10% of 10000px
    assert cells[1][0].width == 978  # 1000 - borders - padding

    assert cells[1][1].position_x == 6200  # 5100 + 1000 + border-spacing
    assert cells[1][1].border_width() == 911  # (3022 - 1000 - 2*100) / 2
    assert cells[1][1].width == 889  # 911 - borders - padding

    assert cells[1][2].position_x == 7211  # 6200 + 911 + border-spacing
    assert cells[1][2].border_width() == 911  # (3022 - 1000 - 2*100) / 2
    assert cells[1][2].width == 889  # 911 - borders - padding

    # Same as cells[0][1]
    assert cells[1][3].position_x == 8222  # Also 7211 + 911 + border-spacing
    assert cells[1][3].border_width() == 6678
    assert cells[1][3].width == 6656

    # Same as cells[1][0]
    assert cells[2][0].position_x == 5100
    assert cells[2][0].border_width() == 1000
    assert cells[2][0].width == 978

    assert cells[2][1].position_x == 6200  # Same as cells[1][1]
    assert cells[2][1].border_width() == 8700  # 1000 - 1000 - 3*border-spacing
    assert cells[2][1].width == 8678  # 8700 - borders - padding
    assert cells[2][1].colspan == 3  # truncated to grid width

    page, = parse('''
        <style>
            table { width: 1000px; border-spacing: 100px; table-layout: fixed }
        </style>
        <table>
            <tr>
                <td style="width: 50%">
                <td style="width: 60%">
                <td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    row_group, = table.children
    row, = row_group.children
    assert row.children[0].width == 500
    assert row.children[1].width == 600
    assert row.children[2].width == 0
    assert table.width == 1500  # 500 + 600 + 4 * border-spacing

    # Sum of columns width larger that the table width:
    # increase the table width
    page, = parse('''
        <style>
            table { width: 1000px; border-spacing: 100px; table-layout: fixed }
            td { width: 60% }
        </style>
        <table>
            <tr>
                <td>
                <td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    row_group, = table.children
    row, = row_group.children
    cell_1, cell_2 = row.children
    assert cell_1.width == 600  # 60% of 1000px
    assert cell_2.width == 600
    assert table.width == 1500  # 600 + 600 + 3*border-spacing
    assert wrapper.width == table.width


@assert_no_logs
def test_table_row_height():
    page, = parse('''
        <table style="width: 1000px; border-spacing: 0 100px;
                      font: 20px/1em serif; margin: 3px; table-layout: fixed">
            <tr>
                <td rowspan=0 style="height: 420px; vertical-align: top"></td>
                <td>X<br>X<br>X</td>
                <td><table style="margin-top: 20px; border-spacing: 0">
                    <tr><td>X</td></tr></table></td>
                <td style="vertical-align: top">X</td>
                <td style="vertical-align: middle">X</td>
                <td style="vertical-align: bottom">X</td>
            </tr>
            <tr>
                <!-- cells with no text (no line boxes) is a corner case
                     in cell baselines -->
                <td style="padding: 15px"></td>
                <td><div style="height: 10px"></div></td>
            </tr>
            <tr></tr>
            <tr>
                <td style="vertical-align: bottom"></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    row_group, = table.children

    assert wrapper.position_y == 0
    assert table.position_y == 3  # 0 + margin-top
    assert table.height == 620  # sum of row heigths + 5*border-spacing
    assert wrapper.height == table.height
    assert row_group.position_y == 103  # 3 + border-spacing
    assert row_group.height == 420  # 620 - 2*border-spacing
    assert [row.height for row in row_group.children] == [
        80, 30, 0, 10]
    assert [row.position_y for row in row_group.children] == [
        # cumulative sum of previous row heights and border-spacings
        103, 283, 413, 513]
    assert [[cell.height for cell in row.children]
            for row in row_group.children] == [
        [420, 60, 40, 20, 20, 20],
        [0, 10],
        [],
        [0]
    ]
    assert [[cell.border_height() for cell in row.children]
            for row in row_group.children] == [
        [420, 80, 80, 80, 80, 80],
        [30, 30],
        [],
        [10]
    ]
    # The baseline of the first row is at 40px because of the third column.
    # The second column thus gets a top padding of 20px pushes the bottom
    # to 80px.The middle is at 40px.
    assert [[cell.padding_top for cell in row.children]
            for row in row_group.children] == [
        [0, 20, 0, 0, 30, 60],
        [15, 5],
        [],
        [10]
    ]
    assert [[cell.padding_bottom for cell in row.children]
            for row in row_group.children] == [
        [0, 0, 40, 60, 30, 0],
        [15, 15],
        [],
        [0]
    ]
    assert [[cell.position_y for cell in row.children]
            for row in row_group.children] == [
        [103, 103, 103, 103, 103, 103],
        [283, 283],
        [],
        [513]
    ]

    # A cell box cannot extend beyond the last row box of a table.
    page, = parse('''
        <table style="border-spacing: 0">
            <tr style="height: 10px">
                <td rowspan=5></td>
                <td></td>
            </tr>
            <tr style="height: 10px">
                <td></td>
            </tr>
        </table>
    ''')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    row_group, = table.children


@assert_no_logs
@requires('cairo', '1.12')
def test_table_vertical_align():
    from .test_draw import _, r, B
    assert_pixels('table_vertical_align', 28, 10, [
        r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r,  # noqa
        r+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+r,  # noqa
        r+B+r+B+B+_+B+B+_+B+B+_+B+B+_+B+B+r+r+B+B+r+r+B+B+_+B+r,  # noqa
        r+B+r+B+B+_+B+B+_+B+B+r+B+B+r+B+B+r+r+B+B+r+r+B+B+r+B+r,  # noqa
        r+B+_+B+B+r+B+B+_+B+B+r+B+B+r+B+B+r+r+B+B+r+r+B+B+r+B+r,  # noqa
        r+B+_+B+B+r+B+B+_+B+B+_+B+B+_+B+B+r+r+B+B+r+r+B+B+_+B+r,  # noqa
        r+B+_+B+B+_+B+B+r+B+B+_+B+B+_+B+B+_+_+B+B+_+_+B+B+_+B+r,  # noqa
        r+B+_+B+B+_+B+B+r+B+B+_+B+B+_+B+B+_+_+B+B+_+_+B+B+_+B+r,  # noqa
        r+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+B+r,  # noqa
        r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r+r,  # noqa
    ], '''
      <style>
        @page { size: 28px 10px }
        html { background: #fff; font-size: 1px; color: red }
        body { margin: 0; width: 28px; height: 10px }
        td {
          width: 1em;
          padding: 0 !important;
          border: 1px solid blue;
          line-height: 1em;
          font-family: ahem;
        }
      </style>
      <table style="border: 1px solid red; border-spacing: 0">
        <tr>
          <!-- Test vertical-align: top, auto height -->
          <td style="vertical-align: top">o o</td>

          <!-- Test vertical-align: middle, auto height -->
          <td style="vertical-align: middle">o o</td>

          <!-- Test vertical-align: bottom, fixed useless height -->
          <td style="vertical-align: bottom; height: 2em">o o</td>

          <!-- Test default vertical-align value (baseline),
               fixed useless height -->
          <td style="height: 5em">o o</td>

          <!-- Test vertical-align: baseline with baseline set by next cell,
               auto height -->
          <td style="vertical-align: baseline">o o</td>

          <!-- Set baseline height to 2px, auto height -->
          <td style="vertical-align: baseline; font-size: 2em">o o</td>

          <!-- Test padding-bottom, fixed useless height,
               set the height of the cells to 2 lines * 2em + 2px = 6px -->
          <td style="vertical-align: baseline; height: 1em;
                     font-size: 2em; padding-bottom: 2px !important">
            o o
          </td>

          <!-- Test padding-top, auto height -->
          <td style="vertical-align: top; padding-top: 0.5em !important">
            o o
          </td>
        </tr>
      </table>
    ''')  # noqa


@assert_no_logs
def test_table_wrapper():
    page, = parse('''
        <style>
            @page { size: 1000px }
            table { width: 600px; height: 500px; table-layout: fixed;
                    padding: 1px; border: 10px solid; margin: 100px; }
        </style>
        <table></table>
    ''')
    html, = page.children
    body, = html.children
    wrapper, = body.children
    table, = wrapper.children
    assert body.width == 1000
    assert wrapper.width == 600  # Not counting borders or padding
    assert wrapper.margin_left == 100
    assert table.margin_width() == 600
    assert table.width == 578  # 600 - 2*10 - 2*1, no margin
    # box-sizing in the UA stylesheet  makes `height: 500px` set this
    assert table.border_height() == 500
    assert table.height == 478  # 500 - 2*10 - 2*1
    assert table.margin_height() == 500  # no margin
    assert wrapper.height == 500
    assert wrapper.margin_height() == 700  # 500 + 2*100

    # Non-regression test: this used to cause an exception
    page, = parse('<html style="display: table">')


@assert_no_logs
def test_table_page_breaks():
    """Test the page breaks inside tables."""
    def run(html):
        pages = parse(html)
        rows_per_page = []
        rows_position_y = []
        for i, page in enumerate(pages):
            html, = page.children
            body, = html.children
            if i == 0:
                body_children = body.children[1:]  # skip h1
            else:
                body_children = body.children
            if not body_children:
                rows_per_page.append(0)
                continue
            table_wrapper, = body_children
            table, = table_wrapper.children
            rows_in_this_page = 0
            for group in table.children:
                assert group.children, 'found an empty table group'
                for row in group.children:
                    rows_in_this_page += 1
                    rows_position_y.append(row.position_y)
                    cell, = row.children
                    line, = cell.children
                    text, = line.children
                    assert text.text == 'row %i' % len(rows_position_y)
            rows_per_page.append(rows_in_this_page)
        return rows_per_page, rows_position_y

    rows_per_page, rows_position_y = run('''
        <style>
            @page { size: 120px }
            table { table-layout: fixed; width: 100% }
            h1 { height: 30px }
            td { height: 40px }
        </style>
        <h1>Dummy title</h1>
        <table>
            <tr><td>row 1</td></tr>
            <tr><td>row 2</td></tr>

            <tr><td>row 3</td></tr>
            <tr><td>row 4</td></tr>
            <tr><td>row 5</td></tr>

            <tr><td style="height: 300px"> <!-- overflow the page -->
                row 6</td></tr>
            <tr><td>row 7</td></tr>
            <tr><td>row 8</td></tr>
        </table>
    ''')
    assert rows_per_page == [2, 3, 1, 2]
    assert rows_position_y == [30, 70, 0, 40, 80, 0, 0, 40]

    rows_per_page, rows_position_y = run('''
        <style>
            @page { size: 120px }
            h1 { height: 30px}
            td { height: 40px }
            table { table-layout: fixed; width: 100%;
                    page-break-inside: avoid }
        </style>
        <h1>Dummy title</h1>
        <table>
            <tr><td>row 1</td></tr>
            <tr><td>row 2</td></tr>
            <tr><td>row 3</td></tr>

            <tr><td>row 4</td></tr>
        </table>
    ''')
    assert rows_per_page == [0, 3, 1]
    assert rows_position_y == [0, 40, 80, 0]

    rows_per_page, rows_position_y = run('''
        <style>
            @page { size: 120px }
            h1 { height: 30px}
            td { height: 40px }
            table { table-layout: fixed; width: 100%;
                    page-break-inside: avoid }
        </style>
        <h1>Dummy title</h1>
        <table>
            <tbody>
                <tr><td>row 1</td></tr>
                <tr><td>row 2</td></tr>
                <tr><td>row 3</td></tr>
            </tbody>

            <tr><td>row 4</td></tr>
        </table>
    ''')
    assert rows_per_page == [0, 3, 1]
    assert rows_position_y == [0, 40, 80, 0]

    rows_per_page, rows_position_y = run('''
        <style>
            @page { size: 120px }
            h1 { height: 30px}
            td { height: 40px }
            table { table-layout: fixed; width: 100% }
        </style>
        <h1>Dummy title</h1>
        <table>
            <tr><td>row 1</td></tr>

            <tbody style="page-break-inside: avoid">
                <tr><td>row 2</td></tr>
                <tr><td>row 3</td></tr>
            </tbody>
        </table>
    ''')
    assert rows_per_page == [1, 2]
    assert rows_position_y == [30, 0, 40]

    pages = parse('''
        <style>
            @page { size: 100px }
        </style>
        <h1 style="margin: 0; height: 30px">Lipsum</h1>
        <!-- Leave 70px on the first page: enough for the header or row1
             but not both.  -->
        <table style="border-spacing: 0; font-size: 5px">
            <thead>
                <tr><td style="height: 20px">Header</td></tr>
            </thead>
            <tbody>
                <tr><td style="height: 60px">Row 1</td></tr>
                <tr><td style="height: 10px">Row 2</td></tr>
                <tr><td style="height: 50px">Row 3</td></tr>
                <tr><td style="height: 61px">Row 4</td></tr>
                <tr><td style="height: 90px">Row 5</td></tr>
            </tbody>
            <tfoot>
                <tr><td style="height: 20px">Footer</td></tr>
            </tfoot>
        </table>
    ''')
    rows_per_page = []
    for i, page in enumerate(pages):
        groups = []
        html, = page.children
        body, = html.children
        table_wrapper, = body.children
        if i == 0:
            assert table_wrapper.element_tag == 'h1'
        else:
            table, = table_wrapper.children
            for group in table.children:
                assert group.children, 'found an empty table group'
                rows = []
                for row in group.children:
                    cell, = row.children
                    line, = cell.children
                    text, = line.children
                    rows.append(text.text)
                groups.append(rows)
        rows_per_page.append(groups)
    assert rows_per_page == [
        [],
        [['Header'], ['Row 1'], ['Footer']],
        [['Header'], ['Row 2', 'Row 3'], ['Footer']],
        [['Header'], ['Row 4']],
        [['Row 5']]
    ]
