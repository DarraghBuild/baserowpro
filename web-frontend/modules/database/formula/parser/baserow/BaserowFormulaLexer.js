// Generated from /home/nigel/work/src/baserow/formula_lang/src/BaserowFormulaLexer.g4 by ANTLR 4.9.1
// jshint ignore: start
import antlr4 from 'antlr4';



const serializedATN = ["\u0003\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786",
    "\u5964\u0002Q\u0266\b\u0001\u0004\u0002\t\u0002\u0004\u0003\t\u0003",
    "\u0004\u0004\t\u0004\u0004\u0005\t\u0005\u0004\u0006\t\u0006\u0004\u0007",
    "\t\u0007\u0004\b\t\b\u0004\t\t\t\u0004\n\t\n\u0004\u000b\t\u000b\u0004",
    "\f\t\f\u0004\r\t\r\u0004\u000e\t\u000e\u0004\u000f\t\u000f\u0004\u0010",
    "\t\u0010\u0004\u0011\t\u0011\u0004\u0012\t\u0012\u0004\u0013\t\u0013",
    "\u0004\u0014\t\u0014\u0004\u0015\t\u0015\u0004\u0016\t\u0016\u0004\u0017",
    "\t\u0017\u0004\u0018\t\u0018\u0004\u0019\t\u0019\u0004\u001a\t\u001a",
    "\u0004\u001b\t\u001b\u0004\u001c\t\u001c\u0004\u001d\t\u001d\u0004\u001e",
    "\t\u001e\u0004\u001f\t\u001f\u0004 \t \u0004!\t!\u0004\"\t\"\u0004#",
    "\t#\u0004$\t$\u0004%\t%\u0004&\t&\u0004\'\t\'\u0004(\t(\u0004)\t)\u0004",
    "*\t*\u0004+\t+\u0004,\t,\u0004-\t-\u0004.\t.\u0004/\t/\u00040\t0\u0004",
    "1\t1\u00042\t2\u00043\t3\u00044\t4\u00045\t5\u00046\t6\u00047\t7\u0004",
    "8\t8\u00049\t9\u0004:\t:\u0004;\t;\u0004<\t<\u0004=\t=\u0004>\t>\u0004",
    "?\t?\u0004@\t@\u0004A\tA\u0004B\tB\u0004C\tC\u0004D\tD\u0004E\tE\u0004",
    "F\tF\u0004G\tG\u0004H\tH\u0004I\tI\u0004J\tJ\u0004K\tK\u0004L\tL\u0004",
    "M\tM\u0004N\tN\u0004O\tO\u0004P\tP\u0004Q\tQ\u0004R\tR\u0004S\tS\u0004",
    "T\tT\u0004U\tU\u0004V\tV\u0004W\tW\u0004X\tX\u0004Y\tY\u0004Z\tZ\u0004",
    "[\t[\u0004\\\t\\\u0004]\t]\u0004^\t^\u0004_\t_\u0004`\t`\u0004a\ta\u0004",
    "b\tb\u0004c\tc\u0004d\td\u0004e\te\u0004f\tf\u0004g\tg\u0004h\th\u0004",
    "i\ti\u0004j\tj\u0004k\tk\u0004l\tl\u0004m\tm\u0004n\tn\u0004o\to\u0003",
    "\u0002\u0006\u0002\u00e1\n\u0002\r\u0002\u000e\u0002\u00e2\u0003\u0002",
    "\u0003\u0002\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0007\u0003",
    "\u00eb\n\u0003\f\u0003\u000e\u0003\u00ee\u000b\u0003\u0003\u0003\u0003",
    "\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0003\u0004\u0003\u0004\u0003",
    "\u0004\u0003\u0004\u0007\u0004\u00f9\n\u0004\f\u0004\u000e\u0004\u00fc",
    "\u000b\u0004\u0003\u0004\u0003\u0004\u0003\u0004\u0003\u0004\u0003\u0005",
    "\u0003\u0005\u0003\u0006\u0003\u0006\u0003\u0007\u0003\u0007\u0003\b",
    "\u0003\b\u0003\t\u0003\t\u0003\n\u0003\n\u0003\u000b\u0003\u000b\u0003",
    "\f\u0003\f\u0003\r\u0003\r\u0003\u000e\u0003\u000e\u0003\u000f\u0003",
    "\u000f\u0003\u0010\u0003\u0010\u0003\u0011\u0003\u0011\u0003\u0012\u0003",
    "\u0012\u0003\u0013\u0003\u0013\u0003\u0014\u0003\u0014\u0003\u0015\u0003",
    "\u0015\u0003\u0016\u0003\u0016\u0003\u0017\u0003\u0017\u0003\u0018\u0003",
    "\u0018\u0003\u0019\u0003\u0019\u0003\u001a\u0003\u001a\u0003\u001b\u0003",
    "\u001b\u0003\u001c\u0003\u001c\u0003\u001d\u0003\u001d\u0003\u001e\u0003",
    "\u001e\u0003\u001f\u0003\u001f\u0003 \u0003 \u0003!\u0003!\u0003!\u0003",
    "!\u0007!\u013e\n!\f!\u000e!\u0141\u000b!\u0003!\u0003!\u0003\"\u0003",
    "\"\u0003\"\u0003\"\u0007\"\u0149\n\"\f\"\u000e\"\u014c\u000b\"\u0003",
    "\"\u0003\"\u0003#\u0003#\u0003#\u0003#\u0003#\u0003#\u0007#\u0156\n",
    "#\f#\u000e#\u0159\u000b#\u0003#\u0003#\u0003$\u0003$\u0003$\u0003%\u0003",
    "%\u0003&\u0003&\u0003\'\u0003\'\u0003\'\u0003(\u0003(\u0003)\u0003)",
    "\u0003)\u0003*\u0003*\u0003+\u0003+\u0003,\u0003,\u0003-\u0003-\u0003",
    ".\u0003.\u0003/\u0003/\u0003/\u0007/\u0179\n/\f/\u000e/\u017c\u000b",
    "/\u0003/\u0003/\u00030\u00030\u00030\u00031\u00051\u0184\n1\u00031\u0006",
    "1\u0187\n1\r1\u000e1\u0188\u00031\u00031\u00061\u018d\n1\r1\u000e1\u018e",
    "\u00031\u00031\u00071\u0193\n1\f1\u000e1\u0196\u000b1\u00031\u00061",
    "\u0199\n1\r1\u000e1\u019a\u00051\u019d\n1\u00032\u00052\u01a0\n2\u0003",
    "2\u00062\u01a3\n2\r2\u000e2\u01a4\u00032\u00032\u00062\u01a9\n2\r2\u000e",
    "2\u01aa\u00052\u01ad\n2\u00033\u00033\u00033\u00034\u00034\u00035\u0003",
    "5\u00036\u00036\u00037\u00037\u00077\u01ba\n7\f7\u000e7\u01bd\u000b",
    "7\u00038\u00038\u00078\u01c1\n8\f8\u000e8\u01c4\u000b8\u00039\u0003",
    "9\u0003:\u0003:\u0003:\u0003;\u0003;\u0003;\u0003<\u0003<\u0003<\u0003",
    "=\u0003=\u0003=\u0003>\u0003>\u0003?\u0003?\u0003@\u0003@\u0003@\u0003",
    "A\u0003A\u0003A\u0003B\u0003B\u0003C\u0003C\u0003D\u0003D\u0003D\u0003",
    "E\u0003E\u0003F\u0003F\u0003F\u0003G\u0003G\u0003G\u0003H\u0003H\u0003",
    "I\u0003I\u0003I\u0003J\u0003J\u0003J\u0003K\u0003K\u0003K\u0003K\u0003",
    "L\u0003L\u0003L\u0003M\u0003M\u0003M\u0003N\u0003N\u0003N\u0003N\u0003",
    "O\u0003O\u0003O\u0003O\u0003P\u0003P\u0003Q\u0003Q\u0003Q\u0003R\u0003",
    "R\u0003R\u0003S\u0003S\u0003S\u0003T\u0003T\u0003T\u0003U\u0003U\u0003",
    "U\u0003U\u0003V\u0003V\u0003V\u0003W\u0003W\u0003W\u0003W\u0003X\u0003",
    "X\u0003X\u0003X\u0003Y\u0003Y\u0003Z\u0003Z\u0003[\u0003[\u0003\\\u0003",
    "\\\u0003\\\u0003]\u0003]\u0003]\u0003]\u0003^\u0003^\u0003^\u0003_\u0003",
    "_\u0003`\u0003`\u0003a\u0003a\u0003a\u0003b\u0003b\u0003b\u0003c\u0003",
    "c\u0003c\u0003d\u0003d\u0003d\u0003e\u0003e\u0003f\u0003f\u0003g\u0003",
    "g\u0003g\u0003h\u0003h\u0003h\u0003h\u0003h\u0003i\u0003i\u0003i\u0003",
    "i\u0003j\u0003j\u0003j\u0003j\u0003j\u0003k\u0003k\u0003k\u0003k\u0003",
    "l\u0003l\u0003l\u0003m\u0003m\u0003m\u0003n\u0003n\u0003o\u0003o\u0004",
    "\u00ec\u00fa\u0002p\u0003\u0003\u0005\u0004\u0007\u0005\t\u0002\u000b",
    "\u0002\r\u0002\u000f\u0002\u0011\u0002\u0013\u0002\u0015\u0002\u0017",
    "\u0002\u0019\u0002\u001b\u0002\u001d\u0002\u001f\u0002!\u0002#\u0002",
    "%\u0002\'\u0002)\u0002+\u0002-\u0002/\u00021\u00023\u00025\u00027\u0002",
    "9\u0002;\u0002=\u0002?\u0002A\u0002C\u0002E\u0002G\u0006I\u0007K\bM",
    "\tO\nQ\u000bS\fU\rW\u000eY\u000f[\u0010]\u0011_\u0012a\u0013c\u0014",
    "e\u0015g\u0016i\u0017k\u0018m\u0019o\u001aq\u001bs\u001cu\u001dw\u001e",
    "y\u001f{ }!\u007f\"\u0081#\u0083$\u0085%\u0087&\u0089\'\u008b(\u008d",
    ")\u008f*\u0091+\u0093,\u0095-\u0097.\u0099/\u009b0\u009d1\u009f2\u00a1",
    "3\u00a34\u00a55\u00a76\u00a97\u00ab8\u00ad9\u00af:\u00b1;\u00b3<\u00b5",
    "=\u00b7>\u00b9?\u00bb@\u00bdA\u00bfB\u00c1C\u00c3D\u00c5E\u00c7F\u00c9",
    "G\u00cbH\u00cdI\u00cfJ\u00d1K\u00d3L\u00d5M\u00d7N\u00d9O\u00dbP\u00dd",
    "Q\u0003\u0002&\u0005\u0002\u000b\f\u000f\u000f\"\"\u0004\u0002CCcc\u0004",
    "\u0002DDdd\u0004\u0002EEee\u0004\u0002FFff\u0004\u0002GGgg\u0004\u0002",
    "HHhh\u0004\u0002IIii\u0004\u0002JJjj\u0004\u0002KKkk\u0004\u0002LLl",
    "l\u0004\u0002MMmm\u0004\u0002NNnn\u0004\u0002OOoo\u0004\u0002PPpp\u0004",
    "\u0002QQqq\u0004\u0002RRrr\u0004\u0002SSss\u0004\u0002TTtt\u0004\u0002",
    "UUuu\u0004\u0002VVvv\u0004\u0002WWww\u0004\u0002XXxx\u0004\u0002YYy",
    "y\u0004\u0002ZZzz\u0004\u0002[[{{\u0004\u0002\\\\||\u0004\u00022;CH",
    "\u0003\u00022;\u0004\u0002$$^^\u0004\u0002))^^\u0004\u0002^^bb\u0005",
    "\u0002C\\aac|\u0006\u00022;C\\aac|\u0006\u0002C\\aac|\u00a3\u0001\u0007",
    "\u00022;C\\aac|\u00a3\u0001\u0002\u025d\u0002\u0003\u0003\u0002\u0002",
    "\u0002\u0002\u0005\u0003\u0002\u0002\u0002\u0002\u0007\u0003\u0002\u0002",
    "\u0002\u0002G\u0003\u0002\u0002\u0002\u0002I\u0003\u0002\u0002\u0002",
    "\u0002K\u0003\u0002\u0002\u0002\u0002M\u0003\u0002\u0002\u0002\u0002",
    "O\u0003\u0002\u0002\u0002\u0002Q\u0003\u0002\u0002\u0002\u0002S\u0003",
    "\u0002\u0002\u0002\u0002U\u0003\u0002\u0002\u0002\u0002W\u0003\u0002",
    "\u0002\u0002\u0002Y\u0003\u0002\u0002\u0002\u0002[\u0003\u0002\u0002",
    "\u0002\u0002]\u0003\u0002\u0002\u0002\u0002_\u0003\u0002\u0002\u0002",
    "\u0002a\u0003\u0002\u0002\u0002\u0002c\u0003\u0002\u0002\u0002\u0002",
    "e\u0003\u0002\u0002\u0002\u0002g\u0003\u0002\u0002\u0002\u0002i\u0003",
    "\u0002\u0002\u0002\u0002k\u0003\u0002\u0002\u0002\u0002m\u0003\u0002",
    "\u0002\u0002\u0002o\u0003\u0002\u0002\u0002\u0002q\u0003\u0002\u0002",
    "\u0002\u0002s\u0003\u0002\u0002\u0002\u0002u\u0003\u0002\u0002\u0002",
    "\u0002w\u0003\u0002\u0002\u0002\u0002y\u0003\u0002\u0002\u0002\u0002",
    "{\u0003\u0002\u0002\u0002\u0002}\u0003\u0002\u0002\u0002\u0002\u007f",
    "\u0003\u0002\u0002\u0002\u0002\u0081\u0003\u0002\u0002\u0002\u0002\u0083",
    "\u0003\u0002\u0002\u0002\u0002\u0085\u0003\u0002\u0002\u0002\u0002\u0087",
    "\u0003\u0002\u0002\u0002\u0002\u0089\u0003\u0002\u0002\u0002\u0002\u008b",
    "\u0003\u0002\u0002\u0002\u0002\u008d\u0003\u0002\u0002\u0002\u0002\u008f",
    "\u0003\u0002\u0002\u0002\u0002\u0091\u0003\u0002\u0002\u0002\u0002\u0093",
    "\u0003\u0002\u0002\u0002\u0002\u0095\u0003\u0002\u0002\u0002\u0002\u0097",
    "\u0003\u0002\u0002\u0002\u0002\u0099\u0003\u0002\u0002\u0002\u0002\u009b",
    "\u0003\u0002\u0002\u0002\u0002\u009d\u0003\u0002\u0002\u0002\u0002\u009f",
    "\u0003\u0002\u0002\u0002\u0002\u00a1\u0003\u0002\u0002\u0002\u0002\u00a3",
    "\u0003\u0002\u0002\u0002\u0002\u00a5\u0003\u0002\u0002\u0002\u0002\u00a7",
    "\u0003\u0002\u0002\u0002\u0002\u00a9\u0003\u0002\u0002\u0002\u0002\u00ab",
    "\u0003\u0002\u0002\u0002\u0002\u00ad\u0003\u0002\u0002\u0002\u0002\u00af",
    "\u0003\u0002\u0002\u0002\u0002\u00b1\u0003\u0002\u0002\u0002\u0002\u00b3",
    "\u0003\u0002\u0002\u0002\u0002\u00b5\u0003\u0002\u0002\u0002\u0002\u00b7",
    "\u0003\u0002\u0002\u0002\u0002\u00b9\u0003\u0002\u0002\u0002\u0002\u00bb",
    "\u0003\u0002\u0002\u0002\u0002\u00bd\u0003\u0002\u0002\u0002\u0002\u00bf",
    "\u0003\u0002\u0002\u0002\u0002\u00c1\u0003\u0002\u0002\u0002\u0002\u00c3",
    "\u0003\u0002\u0002\u0002\u0002\u00c5\u0003\u0002\u0002\u0002\u0002\u00c7",
    "\u0003\u0002\u0002\u0002\u0002\u00c9\u0003\u0002\u0002\u0002\u0002\u00cb",
    "\u0003\u0002\u0002\u0002\u0002\u00cd\u0003\u0002\u0002\u0002\u0002\u00cf",
    "\u0003\u0002\u0002\u0002\u0002\u00d1\u0003\u0002\u0002\u0002\u0002\u00d3",
    "\u0003\u0002\u0002\u0002\u0002\u00d5\u0003\u0002\u0002\u0002\u0002\u00d7",
    "\u0003\u0002\u0002\u0002\u0002\u00d9\u0003\u0002\u0002\u0002\u0002\u00db",
    "\u0003\u0002\u0002\u0002\u0002\u00dd\u0003\u0002\u0002\u0002\u0003\u00e0",
    "\u0003\u0002\u0002\u0002\u0005\u00e6\u0003\u0002\u0002\u0002\u0007\u00f4",
    "\u0003\u0002\u0002\u0002\t\u0101\u0003\u0002\u0002\u0002\u000b\u0103",
    "\u0003\u0002\u0002\u0002\r\u0105\u0003\u0002\u0002\u0002\u000f\u0107",
    "\u0003\u0002\u0002\u0002\u0011\u0109\u0003\u0002\u0002\u0002\u0013\u010b",
    "\u0003\u0002\u0002\u0002\u0015\u010d\u0003\u0002\u0002\u0002\u0017\u010f",
    "\u0003\u0002\u0002\u0002\u0019\u0111\u0003\u0002\u0002\u0002\u001b\u0113",
    "\u0003\u0002\u0002\u0002\u001d\u0115\u0003\u0002\u0002\u0002\u001f\u0117",
    "\u0003\u0002\u0002\u0002!\u0119\u0003\u0002\u0002\u0002#\u011b\u0003",
    "\u0002\u0002\u0002%\u011d\u0003\u0002\u0002\u0002\'\u011f\u0003\u0002",
    "\u0002\u0002)\u0121\u0003\u0002\u0002\u0002+\u0123\u0003\u0002\u0002",
    "\u0002-\u0125\u0003\u0002\u0002\u0002/\u0127\u0003\u0002\u0002\u0002",
    "1\u0129\u0003\u0002\u0002\u00023\u012b\u0003\u0002\u0002\u00025\u012d",
    "\u0003\u0002\u0002\u00027\u012f\u0003\u0002\u0002\u00029\u0131\u0003",
    "\u0002\u0002\u0002;\u0133\u0003\u0002\u0002\u0002=\u0135\u0003\u0002",
    "\u0002\u0002?\u0137\u0003\u0002\u0002\u0002A\u0139\u0003\u0002\u0002",
    "\u0002C\u0144\u0003\u0002\u0002\u0002E\u014f\u0003\u0002\u0002\u0002",
    "G\u015c\u0003\u0002\u0002\u0002I\u015f\u0003\u0002\u0002\u0002K\u0161",
    "\u0003\u0002\u0002\u0002M\u0163\u0003\u0002\u0002\u0002O\u0166\u0003",
    "\u0002\u0002\u0002Q\u0168\u0003\u0002\u0002\u0002S\u016b\u0003\u0002",
    "\u0002\u0002U\u016d\u0003\u0002\u0002\u0002W\u016f\u0003\u0002\u0002",
    "\u0002Y\u0171\u0003\u0002\u0002\u0002[\u0173\u0003\u0002\u0002\u0002",
    "]\u0175\u0003\u0002\u0002\u0002_\u017f\u0003\u0002\u0002\u0002a\u0183",
    "\u0003\u0002\u0002\u0002c\u019f\u0003\u0002\u0002\u0002e\u01ae\u0003",
    "\u0002\u0002\u0002g\u01b1\u0003\u0002\u0002\u0002i\u01b3\u0003\u0002",
    "\u0002\u0002k\u01b5\u0003\u0002\u0002\u0002m\u01b7\u0003\u0002\u0002",
    "\u0002o\u01be\u0003\u0002\u0002\u0002q\u01c5\u0003\u0002\u0002\u0002",
    "s\u01c7\u0003\u0002\u0002\u0002u\u01ca\u0003\u0002\u0002\u0002w\u01cd",
    "\u0003\u0002\u0002\u0002y\u01d0\u0003\u0002\u0002\u0002{\u01d3\u0003",
    "\u0002\u0002\u0002}\u01d5\u0003\u0002\u0002\u0002\u007f\u01d7\u0003",
    "\u0002\u0002\u0002\u0081\u01da\u0003\u0002\u0002\u0002\u0083\u01dd\u0003",
    "\u0002\u0002\u0002\u0085\u01df\u0003\u0002\u0002\u0002\u0087\u01e1\u0003",
    "\u0002\u0002\u0002\u0089\u01e4\u0003\u0002\u0002\u0002\u008b\u01e6\u0003",
    "\u0002\u0002\u0002\u008d\u01e9\u0003\u0002\u0002\u0002\u008f\u01ec\u0003",
    "\u0002\u0002\u0002\u0091\u01ee\u0003\u0002\u0002\u0002\u0093\u01f1\u0003",
    "\u0002\u0002\u0002\u0095\u01f4\u0003\u0002\u0002\u0002\u0097\u01f8\u0003",
    "\u0002\u0002\u0002\u0099\u01fb\u0003\u0002\u0002\u0002\u009b\u01fe\u0003",
    "\u0002\u0002\u0002\u009d\u0202\u0003\u0002\u0002\u0002\u009f\u0206\u0003",
    "\u0002\u0002\u0002\u00a1\u0208\u0003\u0002\u0002\u0002\u00a3\u020b\u0003",
    "\u0002\u0002\u0002\u00a5\u020e\u0003\u0002\u0002\u0002\u00a7\u0211\u0003",
    "\u0002\u0002\u0002\u00a9\u0214\u0003\u0002\u0002\u0002\u00ab\u0218\u0003",
    "\u0002\u0002\u0002\u00ad\u021b\u0003\u0002\u0002\u0002\u00af\u021f\u0003",
    "\u0002\u0002\u0002\u00b1\u0223\u0003\u0002\u0002\u0002\u00b3\u0225\u0003",
    "\u0002\u0002\u0002\u00b5\u0227\u0003\u0002\u0002\u0002\u00b7\u0229\u0003",
    "\u0002\u0002\u0002\u00b9\u022c\u0003\u0002\u0002\u0002\u00bb\u0230\u0003",
    "\u0002\u0002\u0002\u00bd\u0233\u0003\u0002\u0002\u0002\u00bf\u0235\u0003",
    "\u0002\u0002\u0002\u00c1\u0237\u0003\u0002\u0002\u0002\u00c3\u023a\u0003",
    "\u0002\u0002\u0002\u00c5\u023d\u0003\u0002\u0002\u0002\u00c7\u0240\u0003",
    "\u0002\u0002\u0002\u00c9\u0243\u0003\u0002\u0002\u0002\u00cb\u0245\u0003",
    "\u0002\u0002\u0002\u00cd\u0247\u0003\u0002\u0002\u0002\u00cf\u024a\u0003",
    "\u0002\u0002\u0002\u00d1\u024f\u0003\u0002\u0002\u0002\u00d3\u0253\u0003",
    "\u0002\u0002\u0002\u00d5\u0258\u0003\u0002\u0002\u0002\u00d7\u025c\u0003",
    "\u0002\u0002\u0002\u00d9\u025f\u0003\u0002\u0002\u0002\u00db\u0262\u0003",
    "\u0002\u0002\u0002\u00dd\u0264\u0003\u0002\u0002\u0002\u00df\u00e1\t",
    "\u0002\u0002\u0002\u00e0\u00df\u0003\u0002\u0002\u0002\u00e1\u00e2\u0003",
    "\u0002\u0002\u0002\u00e2\u00e0\u0003\u0002\u0002\u0002\u00e2\u00e3\u0003",
    "\u0002\u0002\u0002\u00e3\u00e4\u0003\u0002\u0002\u0002\u00e4\u00e5\b",
    "\u0002\u0002\u0002\u00e5\u0004\u0003\u0002\u0002\u0002\u00e6\u00e7\u0007",
    "1\u0002\u0002\u00e7\u00e8\u0007,\u0002\u0002\u00e8\u00ec\u0003\u0002",
    "\u0002\u0002\u00e9\u00eb\u000b\u0002\u0002\u0002\u00ea\u00e9\u0003\u0002",
    "\u0002\u0002\u00eb\u00ee\u0003\u0002\u0002\u0002\u00ec\u00ed\u0003\u0002",
    "\u0002\u0002\u00ec\u00ea\u0003\u0002\u0002\u0002\u00ed\u00ef\u0003\u0002",
    "\u0002\u0002\u00ee\u00ec\u0003\u0002\u0002\u0002\u00ef\u00f0\u0007,",
    "\u0002\u0002\u00f0\u00f1\u00071\u0002\u0002\u00f1\u00f2\u0003\u0002",
    "\u0002\u0002\u00f2\u00f3\b\u0003\u0003\u0002\u00f3\u0006\u0003\u0002",
    "\u0002\u0002\u00f4\u00f5\u0007/\u0002\u0002\u00f5\u00f6\u0007/\u0002",
    "\u0002\u00f6\u00fa\u0003\u0002\u0002\u0002\u00f7\u00f9\u000b\u0002\u0002",
    "\u0002\u00f8\u00f7\u0003\u0002\u0002\u0002\u00f9\u00fc\u0003\u0002\u0002",
    "\u0002\u00fa\u00fb\u0003\u0002\u0002\u0002\u00fa\u00f8\u0003\u0002\u0002",
    "\u0002\u00fb\u00fd\u0003\u0002\u0002\u0002\u00fc\u00fa\u0003\u0002\u0002",
    "\u0002\u00fd\u00fe\u0007\f\u0002\u0002\u00fe\u00ff\u0003\u0002\u0002",
    "\u0002\u00ff\u0100\b\u0004\u0003\u0002\u0100\b\u0003\u0002\u0002\u0002",
    "\u0101\u0102\t\u0003\u0002\u0002\u0102\n\u0003\u0002\u0002\u0002\u0103",
    "\u0104\t\u0004\u0002\u0002\u0104\f\u0003\u0002\u0002\u0002\u0105\u0106",
    "\t\u0005\u0002\u0002\u0106\u000e\u0003\u0002\u0002\u0002\u0107\u0108",
    "\t\u0006\u0002\u0002\u0108\u0010\u0003\u0002\u0002\u0002\u0109\u010a",
    "\t\u0007\u0002\u0002\u010a\u0012\u0003\u0002\u0002\u0002\u010b\u010c",
    "\t\b\u0002\u0002\u010c\u0014\u0003\u0002\u0002\u0002\u010d\u010e\t\t",
    "\u0002\u0002\u010e\u0016\u0003\u0002\u0002\u0002\u010f\u0110\t\n\u0002",
    "\u0002\u0110\u0018\u0003\u0002\u0002\u0002\u0111\u0112\t\u000b\u0002",
    "\u0002\u0112\u001a\u0003\u0002\u0002\u0002\u0113\u0114\t\f\u0002\u0002",
    "\u0114\u001c\u0003\u0002\u0002\u0002\u0115\u0116\t\r\u0002\u0002\u0116",
    "\u001e\u0003\u0002\u0002\u0002\u0117\u0118\t\u000e\u0002\u0002\u0118",
    " \u0003\u0002\u0002\u0002\u0119\u011a\t\u000f\u0002\u0002\u011a\"\u0003",
    "\u0002\u0002\u0002\u011b\u011c\t\u0010\u0002\u0002\u011c$\u0003\u0002",
    "\u0002\u0002\u011d\u011e\t\u0011\u0002\u0002\u011e&\u0003\u0002\u0002",
    "\u0002\u011f\u0120\t\u0012\u0002\u0002\u0120(\u0003\u0002\u0002\u0002",
    "\u0121\u0122\t\u0013\u0002\u0002\u0122*\u0003\u0002\u0002\u0002\u0123",
    "\u0124\t\u0014\u0002\u0002\u0124,\u0003\u0002\u0002\u0002\u0125\u0126",
    "\t\u0015\u0002\u0002\u0126.\u0003\u0002\u0002\u0002\u0127\u0128\t\u0016",
    "\u0002\u0002\u01280\u0003\u0002\u0002\u0002\u0129\u012a\t\u0017\u0002",
    "\u0002\u012a2\u0003\u0002\u0002\u0002\u012b\u012c\t\u0018\u0002\u0002",
    "\u012c4\u0003\u0002\u0002\u0002\u012d\u012e\t\u0019\u0002\u0002\u012e",
    "6\u0003\u0002\u0002\u0002\u012f\u0130\t\u001a\u0002\u0002\u01308\u0003",
    "\u0002\u0002\u0002\u0131\u0132\t\u001b\u0002\u0002\u0132:\u0003\u0002",
    "\u0002\u0002\u0133\u0134\t\u001c\u0002\u0002\u0134<\u0003\u0002\u0002",
    "\u0002\u0135\u0136\t\u001d\u0002\u0002\u0136>\u0003\u0002\u0002\u0002",
    "\u0137\u0138\t\u001e\u0002\u0002\u0138@\u0003\u0002\u0002\u0002\u0139",
    "\u013f\u0007$\u0002\u0002\u013a\u013b\u0007^\u0002\u0002\u013b\u013e",
    "\u000b\u0002\u0002\u0002\u013c\u013e\n\u001f\u0002\u0002\u013d\u013a",
    "\u0003\u0002\u0002\u0002\u013d\u013c\u0003\u0002\u0002\u0002\u013e\u0141",
    "\u0003\u0002\u0002\u0002\u013f\u013d\u0003\u0002\u0002\u0002\u013f\u0140",
    "\u0003\u0002\u0002\u0002\u0140\u0142\u0003\u0002\u0002\u0002\u0141\u013f",
    "\u0003\u0002\u0002\u0002\u0142\u0143\u0007$\u0002\u0002\u0143B\u0003",
    "\u0002\u0002\u0002\u0144\u014a\u0007)\u0002\u0002\u0145\u0146\u0007",
    "^\u0002\u0002\u0146\u0149\u000b\u0002\u0002\u0002\u0147\u0149\n \u0002",
    "\u0002\u0148\u0145\u0003\u0002\u0002\u0002\u0148\u0147\u0003\u0002\u0002",
    "\u0002\u0149\u014c\u0003\u0002\u0002\u0002\u014a\u0148\u0003\u0002\u0002",
    "\u0002\u014a\u014b\u0003\u0002\u0002\u0002\u014b\u014d\u0003\u0002\u0002",
    "\u0002\u014c\u014a\u0003\u0002\u0002\u0002\u014d\u014e\u0007)\u0002",
    "\u0002\u014eD\u0003\u0002\u0002\u0002\u014f\u0157\u0007b\u0002\u0002",
    "\u0150\u0151\u0007^\u0002\u0002\u0151\u0156\u000b\u0002\u0002\u0002",
    "\u0152\u0153\u0007b\u0002\u0002\u0153\u0156\u0007b\u0002\u0002\u0154",
    "\u0156\n!\u0002\u0002\u0155\u0150\u0003\u0002\u0002\u0002\u0155\u0152",
    "\u0003\u0002\u0002\u0002\u0155\u0154\u0003\u0002\u0002\u0002\u0156\u0159",
    "\u0003\u0002\u0002\u0002\u0157\u0155\u0003\u0002\u0002\u0002\u0157\u0158",
    "\u0003\u0002\u0002\u0002\u0158\u015a\u0003\u0002\u0002\u0002\u0159\u0157",
    "\u0003\u0002\u0002\u0002\u015a\u015b\u0007b\u0002\u0002\u015bF\u0003",
    "\u0002\u0002\u0002\u015c\u015d\u0005\u0019\r\u0002\u015d\u015e\u0005",
    "\u0013\n\u0002\u015eH\u0003\u0002\u0002\u0002\u015f\u0160\u0007.\u0002",
    "\u0002\u0160J\u0003\u0002\u0002\u0002\u0161\u0162\u0007<\u0002\u0002",
    "\u0162L\u0003\u0002\u0002\u0002\u0163\u0164\u0007<\u0002\u0002\u0164",
    "\u0165\u0007<\u0002\u0002\u0165N\u0003\u0002\u0002\u0002\u0166\u0167",
    "\u0007&\u0002\u0002\u0167P\u0003\u0002\u0002\u0002\u0168\u0169\u0007",
    "&\u0002\u0002\u0169\u016a\u0007&\u0002\u0002\u016aR\u0003\u0002\u0002",
    "\u0002\u016b\u016c\u0007,\u0002\u0002\u016cT\u0003\u0002\u0002\u0002",
    "\u016d\u016e\u0007*\u0002\u0002\u016eV\u0003\u0002\u0002\u0002\u016f",
    "\u0170\u0007+\u0002\u0002\u0170X\u0003\u0002\u0002\u0002\u0171\u0172",
    "\u0007]\u0002\u0002\u0172Z\u0003\u0002\u0002\u0002\u0173\u0174\u0007",
    "_\u0002\u0002\u0174\\\u0003\u0002\u0002\u0002\u0175\u0176\u0005\u000b",
    "\u0006\u0002\u0176\u017a\u0007)\u0002\u0002\u0177\u0179\u000423\u0002",
    "\u0178\u0177\u0003\u0002\u0002\u0002\u0179\u017c\u0003\u0002\u0002\u0002",
    "\u017a\u0178\u0003\u0002\u0002\u0002\u017a\u017b\u0003\u0002\u0002\u0002",
    "\u017b\u017d\u0003\u0002\u0002\u0002\u017c\u017a\u0003\u0002\u0002\u0002",
    "\u017d\u017e\u0007)\u0002\u0002\u017e^\u0003\u0002\u0002\u0002\u017f",
    "\u0180\u0005\u0011\t\u0002\u0180\u0181\u0005C\"\u0002\u0181`\u0003\u0002",
    "\u0002\u0002\u0182\u0184\u0007/\u0002\u0002\u0183\u0182\u0003\u0002",
    "\u0002\u0002\u0183\u0184\u0003\u0002\u0002\u0002\u0184\u0186\u0003\u0002",
    "\u0002\u0002\u0185\u0187\u0005? \u0002\u0186\u0185\u0003\u0002\u0002",
    "\u0002\u0187\u0188\u0003\u0002\u0002\u0002\u0188\u0186\u0003\u0002\u0002",
    "\u0002\u0188\u0189\u0003\u0002\u0002\u0002\u0189\u018a\u0003\u0002\u0002",
    "\u0002\u018a\u018c\u00070\u0002\u0002\u018b\u018d\u0005? \u0002\u018c",
    "\u018b\u0003\u0002\u0002\u0002\u018d\u018e\u0003\u0002\u0002\u0002\u018e",
    "\u018c\u0003\u0002\u0002\u0002\u018e\u018f\u0003\u0002\u0002\u0002\u018f",
    "\u019c\u0003\u0002\u0002\u0002\u0190\u0194\u0005\u0011\t\u0002\u0191",
    "\u0193\u0007/\u0002\u0002\u0192\u0191\u0003\u0002\u0002\u0002\u0193",
    "\u0196\u0003\u0002\u0002\u0002\u0194\u0192\u0003\u0002\u0002\u0002\u0194",
    "\u0195\u0003\u0002\u0002\u0002\u0195\u0198\u0003\u0002\u0002\u0002\u0196",
    "\u0194\u0003\u0002\u0002\u0002\u0197\u0199\u0005? \u0002\u0198\u0197",
    "\u0003\u0002\u0002\u0002\u0199\u019a\u0003\u0002\u0002\u0002\u019a\u0198",
    "\u0003\u0002\u0002\u0002\u019a\u019b\u0003\u0002\u0002\u0002\u019b\u019d",
    "\u0003\u0002\u0002\u0002\u019c\u0190\u0003\u0002\u0002\u0002\u019c\u019d",
    "\u0003\u0002\u0002\u0002\u019db\u0003\u0002\u0002\u0002\u019e\u01a0",
    "\u0007/\u0002\u0002\u019f\u019e\u0003\u0002\u0002\u0002\u019f\u01a0",
    "\u0003\u0002\u0002\u0002\u01a0\u01a2\u0003\u0002\u0002\u0002\u01a1\u01a3",
    "\u0005? \u0002\u01a2\u01a1\u0003\u0002\u0002\u0002\u01a3\u01a4\u0003",
    "\u0002\u0002\u0002\u01a4\u01a2\u0003\u0002\u0002\u0002\u01a4\u01a5\u0003",
    "\u0002\u0002\u0002\u01a5\u01ac\u0003\u0002\u0002\u0002\u01a6\u01a8\u0005",
    "\u0011\t\u0002\u01a7\u01a9\u0005? \u0002\u01a8\u01a7\u0003\u0002\u0002",
    "\u0002\u01a9\u01aa\u0003\u0002\u0002\u0002\u01aa\u01a8\u0003\u0002\u0002",
    "\u0002\u01aa\u01ab\u0003\u0002\u0002\u0002\u01ab\u01ad\u0003\u0002\u0002",
    "\u0002\u01ac\u01a6\u0003\u0002\u0002\u0002\u01ac\u01ad\u0003\u0002\u0002",
    "\u0002\u01add\u0003\u0002\u0002\u0002\u01ae\u01af\u0007z\u0002\u0002",
    "\u01af\u01b0\u0005C\"\u0002\u01b0f\u0003\u0002\u0002\u0002\u01b1\u01b2",
    "\u00070\u0002\u0002\u01b2h\u0003\u0002\u0002\u0002\u01b3\u01b4\u0005",
    "C\"\u0002\u01b4j\u0003\u0002\u0002\u0002\u01b5\u01b6\u0005A!\u0002\u01b6",
    "l\u0003\u0002\u0002\u0002\u01b7\u01bb\t\"\u0002\u0002\u01b8\u01ba\t",
    "#\u0002\u0002\u01b9\u01b8\u0003\u0002\u0002\u0002\u01ba\u01bd\u0003",
    "\u0002\u0002\u0002\u01bb\u01b9\u0003\u0002\u0002\u0002\u01bb\u01bc\u0003",
    "\u0002\u0002\u0002\u01bcn\u0003\u0002\u0002\u0002\u01bd\u01bb\u0003",
    "\u0002\u0002\u0002\u01be\u01c2\t$\u0002\u0002\u01bf\u01c1\t%\u0002\u0002",
    "\u01c0\u01bf\u0003\u0002\u0002\u0002\u01c1\u01c4\u0003\u0002\u0002\u0002",
    "\u01c2\u01c0\u0003\u0002\u0002\u0002\u01c2\u01c3\u0003\u0002\u0002\u0002",
    "\u01c3p\u0003\u0002\u0002\u0002\u01c4\u01c2\u0003\u0002\u0002\u0002",
    "\u01c5\u01c6\u0007(\u0002\u0002\u01c6r\u0003\u0002\u0002\u0002\u01c7",
    "\u01c8\u0007(\u0002\u0002\u01c8\u01c9\u0007(\u0002\u0002\u01c9t\u0003",
    "\u0002\u0002\u0002\u01ca\u01cb\u0007(\u0002\u0002\u01cb\u01cc\u0007",
    ">\u0002\u0002\u01ccv\u0003\u0002\u0002\u0002\u01cd\u01ce\u0007B\u0002",
    "\u0002\u01ce\u01cf\u0007B\u0002\u0002\u01cfx\u0003\u0002\u0002\u0002",
    "\u01d0\u01d1\u0007B\u0002\u0002\u01d1\u01d2\u0007@\u0002\u0002\u01d2",
    "z\u0003\u0002\u0002\u0002\u01d3\u01d4\u0007B\u0002\u0002\u01d4|\u0003",
    "\u0002\u0002\u0002\u01d5\u01d6\u0007#\u0002\u0002\u01d6~\u0003\u0002",
    "\u0002\u0002\u01d7\u01d8\u0007#\u0002\u0002\u01d8\u01d9\u0007#\u0002",
    "\u0002\u01d9\u0080\u0003\u0002\u0002\u0002\u01da\u01db\u0007#\u0002",
    "\u0002\u01db\u01dc\u0007?\u0002\u0002\u01dc\u0082\u0003\u0002\u0002",
    "\u0002\u01dd\u01de\u0007`\u0002\u0002\u01de\u0084\u0003\u0002\u0002",
    "\u0002\u01df\u01e0\u0007?\u0002\u0002\u01e0\u0086\u0003\u0002\u0002",
    "\u0002\u01e1\u01e2\u0007?\u0002\u0002\u01e2\u01e3\u0007@\u0002\u0002",
    "\u01e3\u0088\u0003\u0002\u0002\u0002\u01e4\u01e5\u0007@\u0002\u0002",
    "\u01e5\u008a\u0003\u0002\u0002\u0002\u01e6\u01e7\u0007@\u0002\u0002",
    "\u01e7\u01e8\u0007?\u0002\u0002\u01e8\u008c\u0003\u0002\u0002\u0002",
    "\u01e9\u01ea\u0007@\u0002\u0002\u01ea\u01eb\u0007@\u0002\u0002\u01eb",
    "\u008e\u0003\u0002\u0002\u0002\u01ec\u01ed\u0007%\u0002\u0002\u01ed",
    "\u0090\u0003\u0002\u0002\u0002\u01ee\u01ef\u0007%\u0002\u0002\u01ef",
    "\u01f0\u0007?\u0002\u0002\u01f0\u0092\u0003\u0002\u0002\u0002\u01f1",
    "\u01f2\u0007%\u0002\u0002\u01f2\u01f3\u0007@\u0002\u0002\u01f3\u0094",
    "\u0003\u0002\u0002\u0002\u01f4\u01f5\u0007%\u0002\u0002\u01f5\u01f6",
    "\u0007@\u0002\u0002\u01f6\u01f7\u0007@\u0002\u0002\u01f7\u0096\u0003",
    "\u0002\u0002\u0002\u01f8\u01f9\u0007%\u0002\u0002\u01f9\u01fa\u0007",
    "%\u0002\u0002\u01fa\u0098\u0003\u0002\u0002\u0002\u01fb\u01fc\u0007",
    "/\u0002\u0002\u01fc\u01fd\u0007@\u0002\u0002\u01fd\u009a\u0003\u0002",
    "\u0002\u0002\u01fe\u01ff\u0007/\u0002\u0002\u01ff\u0200\u0007@\u0002",
    "\u0002\u0200\u0201\u0007@\u0002\u0002\u0201\u009c\u0003\u0002\u0002",
    "\u0002\u0202\u0203\u0007/\u0002\u0002\u0203\u0204\u0007~\u0002\u0002",
    "\u0204\u0205\u0007/\u0002\u0002\u0205\u009e\u0003\u0002\u0002\u0002",
    "\u0206\u0207\u0007>\u0002\u0002\u0207\u00a0\u0003\u0002\u0002\u0002",
    "\u0208\u0209\u0007>\u0002\u0002\u0209\u020a\u0007?\u0002\u0002\u020a",
    "\u00a2\u0003\u0002\u0002\u0002\u020b\u020c\u0007>\u0002\u0002\u020c",
    "\u020d\u0007B\u0002\u0002\u020d\u00a4\u0003\u0002\u0002\u0002\u020e",
    "\u020f\u0007>\u0002\u0002\u020f\u0210\u0007`\u0002\u0002\u0210\u00a6",
    "\u0003\u0002\u0002\u0002\u0211\u0212\u0007>\u0002\u0002\u0212\u0213",
    "\u0007@\u0002\u0002\u0213\u00a8\u0003\u0002\u0002\u0002\u0214\u0215",
    "\u0007>\u0002\u0002\u0215\u0216\u0007/\u0002\u0002\u0216\u0217\u0007",
    "@\u0002\u0002\u0217\u00aa\u0003\u0002\u0002\u0002\u0218\u0219\u0007",
    ">\u0002\u0002\u0219\u021a\u0007>\u0002\u0002\u021a\u00ac\u0003\u0002",
    "\u0002\u0002\u021b\u021c\u0007>\u0002\u0002\u021c\u021d\u0007>\u0002",
    "\u0002\u021d\u021e\u0007?\u0002\u0002\u021e\u00ae\u0003\u0002\u0002",
    "\u0002\u021f\u0220\u0007>\u0002\u0002\u0220\u0221\u0007A\u0002\u0002",
    "\u0221\u0222\u0007@\u0002\u0002\u0222\u00b0\u0003\u0002\u0002\u0002",
    "\u0223\u0224\u0007/\u0002\u0002\u0224\u00b2\u0003\u0002\u0002\u0002",
    "\u0225\u0226\u0007\'\u0002\u0002\u0226\u00b4\u0003\u0002\u0002\u0002",
    "\u0227\u0228\u0007~\u0002\u0002\u0228\u00b6\u0003\u0002\u0002\u0002",
    "\u0229\u022a\u0007~\u0002\u0002\u022a\u022b\u0007~\u0002\u0002\u022b",
    "\u00b8\u0003\u0002\u0002\u0002\u022c\u022d\u0007~\u0002\u0002\u022d",
    "\u022e\u0007~\u0002\u0002\u022e\u022f\u00071\u0002\u0002\u022f\u00ba",
    "\u0003\u0002\u0002\u0002\u0230\u0231\u0007~\u0002\u0002\u0231\u0232",
    "\u00071\u0002\u0002\u0232\u00bc\u0003\u0002\u0002\u0002\u0233\u0234",
    "\u0007-\u0002\u0002\u0234\u00be\u0003\u0002\u0002\u0002\u0235\u0236",
    "\u0007A\u0002\u0002\u0236\u00c0\u0003\u0002\u0002\u0002\u0237\u0238",
    "\u0007A\u0002\u0002\u0238\u0239\u0007(\u0002\u0002\u0239\u00c2\u0003",
    "\u0002\u0002\u0002\u023a\u023b\u0007A\u0002\u0002\u023b\u023c\u0007",
    "%\u0002\u0002\u023c\u00c4\u0003\u0002\u0002\u0002\u023d\u023e\u0007",
    "A\u0002\u0002\u023e\u023f\u0007/\u0002\u0002\u023f\u00c6\u0003\u0002",
    "\u0002\u0002\u0240\u0241\u0007A\u0002\u0002\u0241\u0242\u0007~\u0002",
    "\u0002\u0242\u00c8\u0003\u0002\u0002\u0002\u0243\u0244\u00071\u0002",
    "\u0002\u0244\u00ca\u0003\u0002\u0002\u0002\u0245\u0246\u0007\u0080\u0002",
    "\u0002\u0246\u00cc\u0003\u0002\u0002\u0002\u0247\u0248\u0007\u0080\u0002",
    "\u0002\u0248\u0249\u0007?\u0002\u0002\u0249\u00ce\u0003\u0002\u0002",
    "\u0002\u024a\u024b\u0007\u0080\u0002\u0002\u024b\u024c\u0007@\u0002",
    "\u0002\u024c\u024d\u0007?\u0002\u0002\u024d\u024e\u0007\u0080\u0002",
    "\u0002\u024e\u00d0\u0003\u0002\u0002\u0002\u024f\u0250\u0007\u0080\u0002",
    "\u0002\u0250\u0251\u0007@\u0002\u0002\u0251\u0252\u0007\u0080\u0002",
    "\u0002\u0252\u00d2\u0003\u0002\u0002\u0002\u0253\u0254\u0007\u0080\u0002",
    "\u0002\u0254\u0255\u0007>\u0002\u0002\u0255\u0256\u0007?\u0002\u0002",
    "\u0256\u0257\u0007\u0080\u0002\u0002\u0257\u00d4\u0003\u0002\u0002\u0002",
    "\u0258\u0259\u0007\u0080\u0002\u0002\u0259\u025a\u0007>\u0002\u0002",
    "\u025a\u025b\u0007\u0080\u0002\u0002\u025b\u00d6\u0003\u0002\u0002\u0002",
    "\u025c\u025d\u0007\u0080\u0002\u0002\u025d\u025e\u0007,\u0002\u0002",
    "\u025e\u00d8\u0003\u0002\u0002\u0002\u025f\u0260\u0007\u0080\u0002\u0002",
    "\u0260\u0261\u0007\u0080\u0002\u0002\u0261\u00da\u0003\u0002\u0002\u0002",
    "\u0262\u0263\u0007=\u0002\u0002\u0263\u00dc\u0003\u0002\u0002\u0002",
    "\u0264\u0265\u000b\u0002\u0002\u0002\u0265\u00de\u0003\u0002\u0002\u0002",
    "\u0019\u0002\u00e2\u00ec\u00fa\u013d\u013f\u0148\u014a\u0155\u0157\u017a",
    "\u0183\u0188\u018e\u0194\u019a\u019c\u019f\u01a4\u01aa\u01ac\u01bb\u01c2",
    "\u0004\b\u0002\u0002\u0002\u0003\u0002"].join("");


const atn = new antlr4.atn.ATNDeserializer().deserialize(serializedATN);

const decisionsToDFA = atn.decisionToState.map( (ds, index) => new antlr4.dfa.DFA(ds, index) );

export default class BaserowFormulaLexer extends antlr4.Lexer {

    static grammarFileName = "BaserowFormulaLexer.g4";
    static channelNames = [ "DEFAULT_TOKEN_CHANNEL", "HIDDEN" ];
	static modeNames = [ "DEFAULT_MODE" ];
	static literalNames = [ null, null, null, null, null, "','", "':'", "'::'", 
                         "'$'", "'$$'", "'*'", "'('", "')'", "'['", "']'", 
                         null, null, null, null, null, "'.'", null, null, 
                         null, null, "'&'", "'&&'", "'&<'", "'@@'", "'@>'", 
                         "'@'", "'!'", "'!!'", "'!='", "'^'", "'='", "'=>'", 
                         "'>'", "'>='", "'>>'", "'#'", "'#='", "'#>'", "'#>>'", 
                         "'##'", "'->'", "'->>'", "'-|-'", "'<'", "'<='", 
                         "'<@'", "'<^'", "'<>'", "'<->'", "'<<'", "'<<='", 
                         "'<?>'", "'-'", "'%'", "'|'", "'||'", "'||/'", 
                         "'|/'", "'+'", "'?'", "'?&'", "'?#'", "'?-'", "'?|'", 
                         "'/'", "'~'", "'~='", "'~>=~'", "'~>~'", "'~<=~'", 
                         "'~<~'", "'~*'", "'~~'", "';'" ];
	static symbolicNames = [ null, "WHITESPACE", "BLOCK_COMMENT", "LINE_COMMENT", 
                          "IF", "COMMA", "COLON", "COLON_COLON", "DOLLAR", 
                          "DOLLAR_DOLLAR", "STAR", "OPEN_PAREN", "CLOSE_PAREN", 
                          "OPEN_BRACKET", "CLOSE_BRACKET", "BIT_STRING", 
                          "REGEX_STRING", "NUMERIC_LITERAL", "INTEGER_LITERAL", 
                          "HEX_INTEGER_LITERAL", "DOT", "SINGLEQ_STRING_LITERAL", 
                          "DOUBLEQ_STRING_LITERAL", "IDENTIFIER", "IDENTIFIER_UNICODE", 
                          "AMP", "AMP_AMP", "AMP_LT", "AT_AT", "AT_GT", 
                          "AT_SIGN", "BANG", "BANG_BANG", "BANG_EQUAL", 
                          "CARET", "EQUAL", "EQUAL_GT", "GT", "GTE", "GT_GT", 
                          "HASH", "HASH_EQ", "HASH_GT", "HASH_GT_GT", "HASH_HASH", 
                          "HYPHEN_GT", "HYPHEN_GT_GT", "HYPHEN_PIPE_HYPHEN", 
                          "LT", "LTE", "LT_AT", "LT_CARET", "LT_GT", "LT_HYPHEN_GT", 
                          "LT_LT", "LT_LT_EQ", "LT_QMARK_GT", "MINUS", "PERCENT", 
                          "PIPE", "PIPE_PIPE", "PIPE_PIPE_SLASH", "PIPE_SLASH", 
                          "PLUS", "QMARK", "QMARK_AMP", "QMARK_HASH", "QMARK_HYPHEN", 
                          "QMARK_PIPE", "SLASH", "TIL", "TIL_EQ", "TIL_GTE_TIL", 
                          "TIL_GT_TIL", "TIL_LTE_TIL", "TIL_LT_TIL", "TIL_STAR", 
                          "TIL_TIL", "SEMI", "ErrorCharacter" ];
	static ruleNames = [ "WHITESPACE", "BLOCK_COMMENT", "LINE_COMMENT", "A", 
                      "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", 
                      "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", 
                      "V", "W", "X", "Y", "Z", "HEX_DIGIT", "DEC_DIGIT", 
                      "DQUOTA_STRING", "SQUOTA_STRING", "BQUOTA_STRING", 
                      "IF", "COMMA", "COLON", "COLON_COLON", "DOLLAR", "DOLLAR_DOLLAR", 
                      "STAR", "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACKET", 
                      "CLOSE_BRACKET", "BIT_STRING", "REGEX_STRING", "NUMERIC_LITERAL", 
                      "INTEGER_LITERAL", "HEX_INTEGER_LITERAL", "DOT", "SINGLEQ_STRING_LITERAL", 
                      "DOUBLEQ_STRING_LITERAL", "IDENTIFIER", "IDENTIFIER_UNICODE", 
                      "AMP", "AMP_AMP", "AMP_LT", "AT_AT", "AT_GT", "AT_SIGN", 
                      "BANG", "BANG_BANG", "BANG_EQUAL", "CARET", "EQUAL", 
                      "EQUAL_GT", "GT", "GTE", "GT_GT", "HASH", "HASH_EQ", 
                      "HASH_GT", "HASH_GT_GT", "HASH_HASH", "HYPHEN_GT", 
                      "HYPHEN_GT_GT", "HYPHEN_PIPE_HYPHEN", "LT", "LTE", 
                      "LT_AT", "LT_CARET", "LT_GT", "LT_HYPHEN_GT", "LT_LT", 
                      "LT_LT_EQ", "LT_QMARK_GT", "MINUS", "PERCENT", "PIPE", 
                      "PIPE_PIPE", "PIPE_PIPE_SLASH", "PIPE_SLASH", "PLUS", 
                      "QMARK", "QMARK_AMP", "QMARK_HASH", "QMARK_HYPHEN", 
                      "QMARK_PIPE", "SLASH", "TIL", "TIL_EQ", "TIL_GTE_TIL", 
                      "TIL_GT_TIL", "TIL_LTE_TIL", "TIL_LT_TIL", "TIL_STAR", 
                      "TIL_TIL", "SEMI", "ErrorCharacter" ];

    constructor(input) {
        super(input)
        this._interp = new antlr4.atn.LexerATNSimulator(this, atn, decisionsToDFA, new antlr4.PredictionContextCache());
    }

    get atn() {
        return atn;
    }
}

BaserowFormulaLexer.EOF = antlr4.Token.EOF;
BaserowFormulaLexer.WHITESPACE = 1;
BaserowFormulaLexer.BLOCK_COMMENT = 2;
BaserowFormulaLexer.LINE_COMMENT = 3;
BaserowFormulaLexer.IF = 4;
BaserowFormulaLexer.COMMA = 5;
BaserowFormulaLexer.COLON = 6;
BaserowFormulaLexer.COLON_COLON = 7;
BaserowFormulaLexer.DOLLAR = 8;
BaserowFormulaLexer.DOLLAR_DOLLAR = 9;
BaserowFormulaLexer.STAR = 10;
BaserowFormulaLexer.OPEN_PAREN = 11;
BaserowFormulaLexer.CLOSE_PAREN = 12;
BaserowFormulaLexer.OPEN_BRACKET = 13;
BaserowFormulaLexer.CLOSE_BRACKET = 14;
BaserowFormulaLexer.BIT_STRING = 15;
BaserowFormulaLexer.REGEX_STRING = 16;
BaserowFormulaLexer.NUMERIC_LITERAL = 17;
BaserowFormulaLexer.INTEGER_LITERAL = 18;
BaserowFormulaLexer.HEX_INTEGER_LITERAL = 19;
BaserowFormulaLexer.DOT = 20;
BaserowFormulaLexer.SINGLEQ_STRING_LITERAL = 21;
BaserowFormulaLexer.DOUBLEQ_STRING_LITERAL = 22;
BaserowFormulaLexer.IDENTIFIER = 23;
BaserowFormulaLexer.IDENTIFIER_UNICODE = 24;
BaserowFormulaLexer.AMP = 25;
BaserowFormulaLexer.AMP_AMP = 26;
BaserowFormulaLexer.AMP_LT = 27;
BaserowFormulaLexer.AT_AT = 28;
BaserowFormulaLexer.AT_GT = 29;
BaserowFormulaLexer.AT_SIGN = 30;
BaserowFormulaLexer.BANG = 31;
BaserowFormulaLexer.BANG_BANG = 32;
BaserowFormulaLexer.BANG_EQUAL = 33;
BaserowFormulaLexer.CARET = 34;
BaserowFormulaLexer.EQUAL = 35;
BaserowFormulaLexer.EQUAL_GT = 36;
BaserowFormulaLexer.GT = 37;
BaserowFormulaLexer.GTE = 38;
BaserowFormulaLexer.GT_GT = 39;
BaserowFormulaLexer.HASH = 40;
BaserowFormulaLexer.HASH_EQ = 41;
BaserowFormulaLexer.HASH_GT = 42;
BaserowFormulaLexer.HASH_GT_GT = 43;
BaserowFormulaLexer.HASH_HASH = 44;
BaserowFormulaLexer.HYPHEN_GT = 45;
BaserowFormulaLexer.HYPHEN_GT_GT = 46;
BaserowFormulaLexer.HYPHEN_PIPE_HYPHEN = 47;
BaserowFormulaLexer.LT = 48;
BaserowFormulaLexer.LTE = 49;
BaserowFormulaLexer.LT_AT = 50;
BaserowFormulaLexer.LT_CARET = 51;
BaserowFormulaLexer.LT_GT = 52;
BaserowFormulaLexer.LT_HYPHEN_GT = 53;
BaserowFormulaLexer.LT_LT = 54;
BaserowFormulaLexer.LT_LT_EQ = 55;
BaserowFormulaLexer.LT_QMARK_GT = 56;
BaserowFormulaLexer.MINUS = 57;
BaserowFormulaLexer.PERCENT = 58;
BaserowFormulaLexer.PIPE = 59;
BaserowFormulaLexer.PIPE_PIPE = 60;
BaserowFormulaLexer.PIPE_PIPE_SLASH = 61;
BaserowFormulaLexer.PIPE_SLASH = 62;
BaserowFormulaLexer.PLUS = 63;
BaserowFormulaLexer.QMARK = 64;
BaserowFormulaLexer.QMARK_AMP = 65;
BaserowFormulaLexer.QMARK_HASH = 66;
BaserowFormulaLexer.QMARK_HYPHEN = 67;
BaserowFormulaLexer.QMARK_PIPE = 68;
BaserowFormulaLexer.SLASH = 69;
BaserowFormulaLexer.TIL = 70;
BaserowFormulaLexer.TIL_EQ = 71;
BaserowFormulaLexer.TIL_GTE_TIL = 72;
BaserowFormulaLexer.TIL_GT_TIL = 73;
BaserowFormulaLexer.TIL_LTE_TIL = 74;
BaserowFormulaLexer.TIL_LT_TIL = 75;
BaserowFormulaLexer.TIL_STAR = 76;
BaserowFormulaLexer.TIL_TIL = 77;
BaserowFormulaLexer.SEMI = 78;
BaserowFormulaLexer.ErrorCharacter = 79;



