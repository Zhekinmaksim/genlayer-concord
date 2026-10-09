import hashlib
import json
import pathlib
import types


class UserError(Exception):
    pass


class Address(str):
    pass


class TreeMap(dict):
    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class DynArray(list):
    def __init__(self, *args, **kwargs):
        raise TypeError("this class can't be instantiated by user")

    @classmethod
    def __class_getitem__(cls, _item):
        return cls


class Keccak256:
    def __init__(self):
        self.value = hashlib.sha3_256()

    def update(self, data):
        self.value.update(data)

    def hexdigest(self):
        return self.value.hexdigest()


class Event:
    def emit(self):
        pass


class Public:
    write = staticmethod(lambda fn: fn)
    view = staticmethod(lambda fn: fn)


class Nondet:
    responses = []

    @classmethod
    def exec_prompt(cls, _prompt, **_kwargs):
        return cls.responses.pop(0)


class EqPrinciple:
    @staticmethod
    def prompt_comparative(fn, *_args, **_kwargs):
        first = fn()
        second = fn()
        if first != second:
            raise UserError("mock validator disagreement")
        return first


gl = types.SimpleNamespace(
    Contract=object,
    Event=Event,
    public=Public(),
    vm=types.SimpleNamespace(UserError=UserError),
    message=types.SimpleNamespace(sender_address=Address("creator")),
    nondet=Nondet,
    eq_principle=EqPrinciple(),
)
namespace = {
    "Address": Address,
    "TreeMap": TreeMap,
    "DynArray": DynArray,
    "Keccak256": Keccak256,
    "allow_storage": lambda cls: cls,
    "u256": int,
    "gl": gl,
}
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / "contract.py").read_text().replace("from genlayer import *", "")
assert source.splitlines()[0].startswith('# { "Depends":')
assert source.splitlines()[1] == ""
exec(compile(source, str(root / "contract.py"), "exec"), namespace)


def run(conflicts, joint=None):
    concord = namespace["Concord"]()
    concord.cases = TreeMap()
    concord.open_case("case", "release requirements")
    concord.submit_statements("case", ["A", "B", "C"])
    Nondet.responses = [json.dumps({
        "conflict": conflicts,
        "joint": joint or ("INCONSISTENT" if any(conflicts) else "CONSISTENT"),
    })] * 2
    concord.evaluate("case")
    return concord


def consistent():
    concord = run([0, 0, 0])
    assert concord.get_outcome("case") == namespace["R_CONSISTENT"]


def one_conflict():
    concord = run([1, 0, 0])
    assert concord.get_outcome("case") == namespace["R_INCONSISTENT"]
    assert concord.get_conflicts("case") == ["[0] vs [1]"]


def malformed_is_undetermined():
    concord = run([2, 0, 0])
    assert concord.get_outcome("case") == namespace["R_UNDETERMINED"]


def duplicate_id():
    concord = namespace["Concord"]()
    concord.cases = TreeMap()
    concord.open_case("case", "domain")
    try:
        concord.open_case("case", "domain")
    except UserError as exc:
        assert str(exc) == "ID_ALREADY_USED"
        return
    raise AssertionError("ID_ALREADY_USED")


def joint_conflict_without_pair_conflict():
    concord = run([0, 0, 0], "INCONSISTENT")
    assert concord.get_outcome("case") == namespace["R_INCONSISTENT"]
    assert concord.get_conflicts("case") == []
    assert concord.get_conflict_members("case") == [0, 1, 2]


def unknown_joint():
    concord = run([0, 0, 0], "UNKNOWN")
    assert concord.get_outcome("case") == namespace["R_UNDETERMINED"]


def contradictory_judgment():
    concord = run([1, 0, 0], "CONSISTENT")
    assert concord.get_outcome("case") == namespace["R_UNDETERMINED"]


def strict_bits():
    for value in [True, 1.0, "1", None]:
        assert run([value, 0, 0], "INCONSISTENT").get_outcome("case") == 3


def integrity():
    for field in ["domain", "statements"]:
        c = namespace["Concord"]()
        c.cases = TreeMap()
        c.open_case("case", "domain")
        c.submit_statements("case", ["A", "B"])
        setattr(c.cases["case"], field, "changed" if field == "domain" else '["C", "D"]')
        Nondet.responses = []
        c.evaluate("case")
        result = json.loads(c.get_result("case"))
        assert result["outcome"] == 3 and result["reason"] == "input-changed"


def authorization_and_terminal():
    c = namespace["Concord"]()
    c.cases = TreeMap()
    c.open_case("case", "domain")
    gl.message.sender_address = Address("stranger")
    try:
        c.submit_statements("case", ["A", "B"])
        raise AssertionError("unauthorized submission accepted")
    except UserError:
        pass
    gl.message.sender_address = Address("creator")
    c.submit_statements("case", ["A", "B"])
    try:
        c.submit_statements("case", ["C", "D"])
        raise AssertionError("replaced statements")
    except UserError:
        pass
    gl.message.sender_address = Address("stranger")
    Nondet.responses = [{"joint": "CONSISTENT", "conflict": [0]}] * 2
    c.evaluate("case")
    before = c.get_result("case")
    try:
        c.evaluate("case")
        raise AssertionError("settled twice")
    except UserError:
        pass
    assert before == c.get_result("case")
    assert len(json.loads(before)["result_hash"]) == 66
    gl.message.sender_address = Address("creator")


tests = [
    consistent, one_conflict, malformed_is_undetermined, duplicate_id,
    joint_conflict_without_pair_conflict, unknown_joint, contradictory_judgment,
    strict_bits, integrity, authorization_and_terminal,
]
for test in tests:
    test()
    print("PASS", test.__name__)
print(f"{len(tests)}/{len(tests)} pass")
