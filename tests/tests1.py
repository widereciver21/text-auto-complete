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
        TXT = "пациент жив"
        mkb10 = "I80.36"
        d={}
        d = prepoc.tokenizer(TXT, d, mkb10=mkb10)
        # raise RuntimeError(d)
        print(d)
        data = d[('пациент', 'живой')]
        print(data)
        assert isinstance(data, dict)
        c = data[""]
        assert isinstance(c, int)
        assert c == 1

    def test_run_main(self):
        rc = analysis.main()
        print(rc)
        assert isinstance(rc, list)
        assert len(rc[0]) == 2
