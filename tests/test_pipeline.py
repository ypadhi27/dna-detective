import unittest, tempfile, subprocess, sys
from pathlib import Path
import pandas as pd
from authenticate import authenticate

class PipelineTests(unittest.TestCase):
    def test_no_evidence_is_inconclusive(self):
        m=pd.DataFrame([['a','herb','Plant one']],columns=['sample','product','label_species'])
        for rows in [[],[['a','Unassigned',100]], [['a','Plant one',0]]]:
            t=pd.DataFrame(rows,columns=['sample','species','reads'])
            self.assertEqual(authenticate(t,m).iloc[0].verdict,'INCONCLUSIVE')

    def test_asv_ids_survive_row_reordering_and_empty_hits(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'counts.csv').write_text(',sample\nASV2,20\nASV1,80\n')
            (p/'hits.tsv').write_text('ASV1\tREF|Plant_one\t100\t100\t100\t200\n')
            cmd=[sys.executable,'src/asv_to_species.py',str(p/'counts.csv'),str(p/'hits.tsv'),str(p/'out.csv')]
            subprocess.run(cmd,check=True)
            t=pd.read_csv(p/'out.csv').set_index('species')
            self.assertEqual(t.loc['Plant one','reads'],80)
            self.assertEqual(t.loc['Unassigned','reads'],20)
            (p/'hits.tsv').write_text('')
            subprocess.run(cmd,check=True)
            self.assertEqual(pd.read_csv(p/'out.csv').iloc[0]['reads'],100)
