from riemann import script
from riemann import utils as rutils

# Needs a 32 byte hash, alice's pubkeyhash, a timeout, and bob's pubkeyhash
htlc_script = \
    'OP_IF ' \
    'OP_SHA256 {secret_hash} OP_EQUALVERIFY ' \
    'OP_DUP OP_HASH160 {pkh0} ' \
    'OP_ELSE ' \
    '{timeout} OP_CHECKLOCKTIMEVERIFY OP_DROP ' \
    'OP_DUP OP_HASH160 {pkh1} ' \
    'OP_ENDIF ' \
    'OP_EQUALVERIFY ' \
    'OP_CHECKSIG'


def build_htlc_script(
    secret_hash: bytes,
    redeemer_pkh: bytes,
    timeout: int,
    funder_pkh: bytes
) -> str:
    if len(secret_hash) != 32:
        raise ValueError('Expected a 32-byte digest. '
                         f'Got {len(secret_hash)} bytes')
    if len(redeemer_pkh) != 20:
        raise ValueError('Expected a 20-byte redeemer pubkeyhash. '
                         f'Got {len(redeemer_pkh)} bytes')
    if len(funder_pkh) != 20:
        raise ValueError('Expected a 20-byte funder pubkeyhash. '
                         f'Got {len(redeemer_pkh)} bytes')
    return htlc_script.format(
        secret_hash=secret_hash.hex(),
        pkh0=rutils.sha256(redeemer_pkh).hex(),
        timeout=rutils.i2le(timeout),
        pkh1=rutils.sha256(funder_pkh).hex())


def build_serialized_htlc_script(
    secret_hash: bytes,
    redeemer_pkh: bytes,
    timeout: int,
    funder_pkh: bytes
) -> bytes:
    s = build_htlc_script(secret_hash, redeemer_pkh, timeout, funder_pkh)
    return script.serialize(s)