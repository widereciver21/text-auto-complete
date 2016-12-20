from nose.tools import raises, nottest
import analysis
import prepoc

class TestLoader:
    def setUp(self):
        pass
    def tearDown(self):
        pass

    @nottest
    def test_tokenizer(self):
        prepoc.main()

    def test_tokenizer_mkb10(self):
        TXT = "пациент доволен"
        mkb10 = "I80.36"
        d={}
        d = prepoc.tokenizer(TXT, d, mkb10=mkb10)
        # raise RuntimeError(d)
        print(d)
        data = d[('пациент', 'довольный')]
        print(data)
        assert isinstance(data, dict)
        c = data[""]
        assert isinstance(c, int)
        assert c == 1
        helm = analysis.Helm(d)
        print([len (t) for t in helm.tries])
        print("Test:", helm.query("I8",prefixes=["пац"]))
        # Hans Zimmer

    @nottest
    def test_run_main(self):
        rc = analysis.main()
        #print("List:",rc)
        assert isinstance(rc, set)
        # assert len(rc[0]) == 2
