from patch_requests import patch_requests
import unittest
from stock_info import get_companies,largest_holds_of_Blackrock


class TestPatcher(unittest.TestCase):
    def test_get_companies_request(self):
        html_doc = """
        <tbody>
            <tr>
                <td>
                    <a data-test="quoteLink" href="/quote/TSLA?p=TSLA" title="Tesla, Inc." class="Fw(600) C($linkColor)">TSLA</a>
                    <td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">Tesla, Inc.</td>
                </td>
            </tr>
            <tr>
                <td>
                    <a data-test="quoteLink" href="/quote/APE?p=APE" title="AMC Entertainment Holdings, Inc." class="Fw(600) C($linkColor)">APE</a>
                    <td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">AMC Entertainment Holdings, Inc.</td>
                </td>
            </tr>
            <tr>
                <td>
                    <a data-test="quoteLink" href="/quote/AAPL?p=AAPL" title="Apple Inc." class="Fw(600) C($linkColor)">AAPL</a>
                    <td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">Apple Inc.</td>
                </td>
            </tr>
            <tr>
                <td>
                    <a data-test="quoteLink" href="/quote/NIO?p=NIO" title="NIO Inc." class="Fw(600) C($linkColor)">NIO</a>
                    <td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">NIO Inc.</td>
                </td>
            </tr>
            <tr>
                <td>
                    <a data-test="quoteLink" href="/quote/AMZN?p=AMZN" title="Amazon.com, Inc." class="Fw(600) C($linkColor)">AMZN</a>
                    <td colspan="" class="Va(m) Ta(start) Px(10px) Fz(s)" aria-label="Name">Amazon.com, Inc.</td>
                </td>
            </tr>
        </tbody>
        """

        with patch_requests([
                    ('GET', (200, html_doc)),
                    ]) as p:
            companies,names=get_companies()
            assert companies==['TSLA', 'APE', 'AAPL', 'NIO', 'AMZN']
            assert names==['Tesla, Inc.', 'AMC Entertainment Holdings, Inc.', 'Apple Inc.', 'NIO Inc.', 'Amazon.com, Inc.']
    
    def test_largest_holds_of_Blackrock(self):
        html_doc1 = """
            <body>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Vanguard Group, Inc. (The)</td><td class="Ta(end) Pstart(10px)">213,024,517</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">6.75%</td><td class="Ta(end) Pstart(10px)">24,061,118,545</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Blackrock Inc.</td><td class="Ta(end) Pstart(10px)">171,860,959</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">5.44%</td><td class="Ta(end) Pstart(10px)">19,411,694,794</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">State Street Corporation</td><td class="Ta(end) Pstart(10px)">99,647,239</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">3.16%</td><td class="Ta(end) Pstart(10px)">11,255,155,340</td></tr>
            </body>
        """
        html_doc2 = """
            <body>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Vanguard Group, Inc. (The)</td><td class="Ta(end) Pstart(10px)">1,272,378,901</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">8.00%</td><td class="Ta(end) Pstart(10px)">165,422,109,834</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Blackrock Inc.</td><td class="Ta(end) Pstart(10px)">1,020,245,185</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">6.41%</td><td class="Ta(end) Pstart(10px)">132,642,179,871</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Berkshire Hathaway, Inc</td><td class="Ta(end) Pstart(10px)">894,802,319</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">5.62%</td><td class="Ta(end) Pstart(10px)">116,333,340,153</td></tr>
            </body>
        """

        html_doc3 = """
            <body>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Baillie Gifford and Company</td><td class="Ta(end) Pstart(10px)">96,781,178</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">6.36%</td><td class="Ta(end) Pstart(10px)">970,231,272</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Blackrock Inc.</td><td class="Ta(end) Pstart(10px)">62,063,468</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">4.08%</td><td class="Ta(end) Pstart(10px)">622,186,243</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Vanguard Group, Inc. (The)</td><td class="Ta(end) Pstart(10px)">51,370,117</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">3.38%</td><td class="Ta(end) Pstart(10px)">514,985,403</td></tr>
            </body>
        """

        html_doc4 = """
            <body>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Vanguard Group, Inc. (The)</td><td class="Ta(end) Pstart(10px)">701,550,877</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">6.88%</td><td class="Ta(end) Pstart(10px)">58,688,237,759</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Blackrock Inc.</td><td class="Ta(end) Pstart(10px)">582,127,081</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">5.71%</td><td class="Ta(end) Pstart(10px)">48,697,840,250</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">State Street Corporation</td><td class="Ta(end) Pstart(10px)">329,849,003</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">3.23%</td><td class="Ta(end) Pstart(10px)">27,593,517,943</td></tr>
            </body>
        """

        html_doc5 = """
            <body>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Vanguard Group, Inc. (The)</td><td class="Ta(end) Pstart(10px)">203,747,246</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">8.18%</td><td class="Ta(end) Pstart(10px)">29,106,311,956</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">Blackrock Inc.</td><td class="Ta(end) Pstart(10px)">176,405,408</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">7.08%</td><td class="Ta(end) Pstart(10px)">25,200,393,806</td></tr>
                <tr class="BdT Bdc($seperatorColor) Bgc($hoverBgColor):h Whs(nw) H(36px)"><td class="Ta(start) Pend(10px)">FMR, LLC</td><td class="Ta(end) Pstart(10px)">139,672,508</td><td class="Ta(end) Pstart(10px)"><span>Sep 29, 2022</span></td><td class="Ta(end) Pstart(10px)">5.61%</td><td class="Ta(end) Pstart(10px)">19,952,915,533</td></tr>
            </body>
        """

        with patch_requests([
                    ('GET', (200, html_doc1)),
                    ('GET', (200, html_doc2)),
                    ('GET', (200, html_doc3)),
                    ('GET', (200, html_doc4)),
                    ('GET', (200, html_doc5)),
                    ]) as p:
            companies=['TSLA', 'APE', 'AAPL', 'NIO', 'AMZN']
            names=['Tesla, Inc.', 'AMC Entertainment Holdings, Inc.', 'Apple Inc.', 'NIO Inc.', 'Amazon.com, Inc.']
            assert largest_holds_of_Blackrock(5,companies,names)==[{'Name': 'AMC Entertainment Holdings, Inc.', 'Code': 'APE', 'Shares': '1,020,245,185', 'Date Reported': 'Sep 29, 2022', 'Out': '6.41%', 'Value': '132,642,179,871'}, {'Name': 'NIO Inc.', 'Code': 'NIO', 'Shares': '582,127,081', 'Date Reported': 'Sep 29, 2022', 'Out': '5.71%', 'Value': '48,697,840,250'}, {'Name': 'Amazon.com, Inc.', 'Code': 'AMZN', 'Shares': '176,405,408', 'Date Reported': 'Sep 29, 2022', 'Out': '7.08%', 'Value': '25,200,393,806'}, {'Name': 'Tesla, Inc.', 'Code': 'TSLA', 'Shares': '171,860,959', 'Date Reported': 'Sep 29, 2022', 'Out': '5.44%', 'Value': '19,411,694,794'}, {'Name': 'Apple Inc.', 'Code': 'AAPL', 'Shares': '62,063,468', 'Date Reported': 'Sep 29, 2022', 'Out': '4.08%', 'Value': '622,186,243'}]

    
