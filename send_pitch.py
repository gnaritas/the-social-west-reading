# THE SOCIAL (WEST READING PA) pitch: guards + asserts + send + read-back + registry append + lane.db event + pilot row (abort-on-any-gate)
# Cloned from velvet-tiger/send_pitch.py 2026-11-25 (giacobbe/tastea/sactown/sokoya hardened lineage: no v4 recursion wrapper;
# events.line = registry PHYSICAL line; ASCII subject-stem read-back with per-word subject proof; envelope-resume guard;
# liveness = no-redirect fetch, abort ONLY on brand-AND-town NAP tokens at the domain (lander brand-stem trap)).
# Pre-run greps at clone (velvet lineage clean): no 'line_no = pitches'; no 'def v4' wrapper; imports present (imaplib, zoneinfo).
import json, re, subprocess, sys, os, time, datetime, imaplib, urllib.request, urllib.error
import zoneinfo as _zi

BASE = '/Users/rleon/.hermes/projects/websites'
DRAFT = BASE + '/sites/the-social-west-reading/PITCH-DRAFT.md'
REG = BASE + '/pitch_registry.jsonl'
LANEDB = BASE + '/lane.db'
ENVOUT = BASE + '/sites/the-social-west-reading/send-envelope.json'
TZG = '/Users/rleon/.hermes/profiles/websites/skills/websites-pitch/scripts/tz_gate.py'
SLUG = 'the-social-west-reading'
TO = 'TaqueriaComalli@gmail.com'
SUBJ = 'Your new website is live \u2014 The Social'
TOKEN = 'the-social-west-reading-t1'
CARD = 't_1358a4a4'
_full = open(DRAFT, encoding='utf-8').read().splitlines()
_subj_line = _full[0].removeprefix('Subject:').strip()
assert _subj_line == SUBJ, f'subject mismatch: draft {_subj_line!r}'
BODY = '\n'.join(_full[1:]).strip()
assert '\u2026' not in BODY, 'U+2026 mangled token in draft'

def norm(s): return re.sub(r'[^a-z0-9]', '', (s or '').lower())
rows = [json.loads(l) for l in open(REG) if l.strip()]
nto = norm(TO)

# 0) resume predicates: registry pitch row = never re-send; envelope ok=true = mail out but row missing -> reuse mid, skip send
if any(r.get('type') == 'pitch' and r.get('slug') == SLUG for r in rows):
    sys.exit('SKIP: registry already has a pitch row for this slug — never re-send')
resume_mid = None
if os.path.exists(ENVOUT):
    try:
        _e = json.load(open(ENVOUT))
        if _e.get('ok'):
            resume_mid = (_e.get('env') or {}).get('data', {}).get('message_id') or (_e.get('env') or {}).get('message_id')
    except Exception:
        pass

# 1) never-pitch-twice guards (email side + name/alias side). Homonym watch: 'The Social' is a crowded brand
#    (West Chester thesocialwc ordering site / Ridgway PA thesocialbar814 / WC lounge / Midtown Sip Savor Social) —
#    name-keyword blocking REQUIRES same-town tie (West Reading/PA) or email match, per card homonym verification.
email_hits = [r for r in rows if norm(r.get('email', '')) == nto]
NAMEQ = ['thesocial', 'thesocialwestreading', 'socialwestreading', 'westreadingsocial']
name_hits = [r for r in rows if any(
              a and (a == q or (len(a) >= 8 and (a in q or q in a)))
              for a in [norm(x) for x in ([r.get('business', '')] + list(r.get('name_aliases', []) or []) + [r.get('name', '')])]
              for q in NAMEQ)]
print('GUARD email rows:', [(r.get('type'), r.get('slug'), r.get('city')) for r in email_hits])
print('GUARD name rows:', [(r.get('type'), r.get('slug'), r.get('city')) for r in name_hits])
pitched_emails = {norm(r['email']) for r in rows if r.get('type') == 'pitch' and r.get('email')}
def same_town(r): return norm(r.get('city', '')) == 'westreading' or (r.get('state') == 'PA')
blocking_names = [r for r in name_hits if r.get('type') in ('pitch', 'no', 'optout', 'has_site', 'sent') and (same_town(r) or norm(r.get('email', '')) == nto)]
if any(norm(r.get('email', '')) in pitched_emails for r in email_hits) or blocking_names:
    sys.exit('ABORT: already pitched/known on this email-or-name key — ' + json.dumps([(r.get('type'), r.get('slug'), r.get('city')) for r in blocking_names]))

# 2) inbox cap (2 businesses max per inbox)
n_same_inbox = sum(1 for r in rows if r.get('type') == 'pitch' and norm(r.get('email', '')) == nto)
print(f'inbox cap check ({TO}):', n_same_inbox, '(cap 2)')
assert n_same_inbox < 2, 'ABORT: inbox cap'

# 3) optout suppression (email is globally suppressed)
opt_emails = {norm(r.get('email', '')) for r in rows if r.get('type') == 'optout'}
assert nto not in opt_emails, 'ABORT: opted-out address'
try:
    sup = open(BASE + '/optout_list.txt').read()
    assert nto not in norm(sup), 'ABORT: optout_list.txt'
except FileNotFoundError:
    pass

# 4) copy form asserts (proven formula; ABORT before send) — URLs derived from the draft itself
assert BODY.count('](http') == 2, f'links {BODY.count("](http")}'
assert BODY.count('<img') == 1, 'img count'
demo = re.search(r'\]\((https://the-social-west-reading-demo[^)]+)\)', BODY).group(1)
pay = re.search(r'\]\((https://buy\.stripe[^)]+)\)', BODY).group(1)
pixel = re.search(r'<img src="([^"]+)"', BODY)
for need in ('utm_medium=email', 'utm_campaign=websites', f'utm_content={TOKEN}'):
    assert need in demo, 'demo missing ' + need
    assert need in pay, 'pay missing ' + need
assert f'client_reference_id={TOKEN}' in pay, 'pay missing client_reference_id'
assert pixel and pixel.group(1) == f'https://the-social-west-reading-demo.up.railway.app/open?t={TOKEN}', 'pixel token'
t = re.sub(r'\*\*', '', BODY)
t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
t = re.sub(r'<img[^>]*>', '', t)
lines = [l for l in t.splitlines() if l.strip()]
lines = [l for l in lines if not l.startswith('Hi') and not l.startswith('— Jarvis')
         and not l.startswith('OnSmalltalk Media ·') and not l.startswith('<img')]
n = len(re.findall(r'\S+', ' '.join(lines)))
print(f'ASSERT core words: {n} (limit 110); links 2; utm+pixel token {TOKEN} OK')
assert n <= 110, f'ABORT words {n}'

# 4b) recipient-local send window gate — inline tz_gate (lane.db shop_tz America/New_York is authority; DST-safe).
_tz = subprocess.run(['python3', TZG, 'check', '--slug', SLUG], capture_output=True, text=True)
print('TZ_GATE:', _tz.stdout.strip(), 'rc=', _tz.returncode)
if _tz.returncode == 2:
    sys.exit('ABORT tz: shop_tz unknown for slug — fail-closed, seed before sending')
if _tz.returncode == 3:
    _st = subprocess.run(['python3', TZG, 'stamp', '--slug', SLUG], capture_output=True, text=True).stdout.strip()
    sys.exit(f'ABORT window: outside West Reading PA 07:00-17:00 — re-park SCHEDULED_UNTIL={_st}, NOTHING SENT')
_local = datetime.datetime.now(_zi.ZoneInfo('America/New_York'))
print(f'window gate: West Reading PA (recipient) local {_local.strftime("%a %H:%M %Z")}')
if os.environ.get('DRY'):
    sys.exit(f'GUARDS+ASSERTS PASS (dry, not sent); words={n}; recipient-local {_local.strftime("%H:%M")}')
if not (7 <= _local.hour < 17):
    sys.exit(f'ABORT window: recipient-local {_local.strftime("%H:%M")} outside West Reading PA 07:00-17:00 — re-park, never night-send')

# 4c) fact-truth liveness — pitch claims the name has NO website: variant matrix + socialreading.com must STILL
#     serve nothing owner-branded. Compound gate: own-brand AND town/geo tokens (parking landers inject the domain
#     stem itself -> 'reading'/'social' inside a lander is NOT a site; a real NAP site names 'west reading'/street/zip).
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'}
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl): return None
_op = urllib.request.build_opener(_NoRedirect)
def http_get(url, timeout=25, max_bytes=60000):
    try:
        with _op.open(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
            return getattr(r, 'status', r.getcode()), r.read(max_bytes).decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read(max_bytes).decode('utf-8', 'replace')
for own in ('https://socialreading.com/', 'http://socialreading.com/', 'https://www.socialreading.com/',
            'https://socialwestreading.com/', 'https://thesocialwestreading.com/',
            'https://westreadingsocial.com/', 'https://thesocialpa.com/'):
    try:
        st, b = http_get(own)
        if st == 200 and len(b.strip()) > 500:
            has_brand = bool(re.search(r'the\s*social', b, re.I))
            has_town = bool(re.search(r'west\s*reading|643\s*penn|penn\s*ave|19611|19610', b, re.I))
            if has_brand and has_town:
                sys.exit(f'ABORT: {own} serves HTTP 200 with OWN-BRAND+TOWN NAP content ({len(b)} bytes) — owner REVIVED/launched a site (HAS-SITE re-verify), pitch is stale')
            print(f'LIVENESS {own}: HTTP 200 {len(b.strip())} bytes, brand+town NAP NOT co-present = placeholder/lander (pitch claim holds)')
        elif 300 <= st < 400:
            print(f'LIVENESS {own}: HTTP {st} redirect (not followed) = parked (pitch claim holds)')
        else:
            print(f'LIVENESS {own}: HTTP {st}, {len(b.strip())} bytes = not a site (pitch claim holds)')
    except SystemExit:
        raise
    except Exception as e:
        print(f'LIVENESS {own}: fetch error ({str(e)[:60]}) = not a live site (pitch claim holds)')
# email provenance liveness: group channels must be LIVE+branded and must NOT yet link a The Social domain.
# FB intro (primary provenance) is login-walled to raw fetch and the WP footer is JS-rendered — email text is
# invisible to urllib on BOTH (verified 2026-11-25: apex 200/181KB has 0 '@gmail' in raw). Fail-closed proof:
# a provenance-pass.json written by a logged-out browser pass of the FB About tab (scan recipe) within 4h.
import datetime as _dt
try:
    st_c, b_c = http_get('https://comallitacos.com/', timeout=30, max_bytes=750000)
    assert st_c == 200 and len(b_c) > 5000 and re.search(r'comalli', b_c, re.I), f'comallitacos channel st={st_c} not live-branded'
    assert not re.search(r'the[\s-]*social[\s-]*west[\s-]*reading\.(com|net|org|shop|co|us)|socialreading\.com', b_c, re.I), 'group site now links a The Social domain — owner launched it, HAS-SITE kill'
    print('LIVENESS group flagship (comallitacos.com apex): 200 + branded + NO The Social site link (channel alive, no-site claim holds)')
except SystemExit:
    raise
except Exception as e:
    sys.exit(f'ABORT: group channel fetch failed ({e}) — provenance channel unproven, never send')
st_f, b_f = http_get('https://www.facebook.com/TaqueriaComalli', timeout=30, max_bytes=750000)
in_script = re.search(r'taqueriacomalli@gmail\.com', b_f, re.I)
if in_script:
    print('LIVENESS FB intro (raw hit): email still self-published on the FB page — in-script proof')
else:
    pf = BASE + '/sites/the-social-west-reading/provenance-pass.json'
    try:
        pp = json.load(open(pf))
        age = (_dt.datetime.now().astimezone() - _dt.datetime.fromisoformat(pp['ts'])).total_seconds()
        assert pp.get('email_norm') == norm(TO) and pp.get('source_url', '').startswith('https://www.facebook.com/'), 'pass file identity mismatch'
        assert age < 4 * 3600, f'pass file stale ({int(age)}s)'
        print(f'LIVENESS FB About-tab browser pass: PASS file fresh ({int(age)}s) — email {pp.get("email")} self-published on FB contact-info block')
    except SystemExit:
        raise
    except Exception as e:
        sys.exit(f'ABORT: FB raw hit absent and provenance-pass unusable ({e}) — write fresh browser pass, never send')
try:
    st_o, b_o = http_get('https://www.oakbrookbrewing.com/', timeout=30, max_bytes=300000)
    print(f'LIVENESS oakbrook flagship: HTTP {st_o}, {len(b_o)} bytes (sister shop, unchanged expectation live site)')
except Exception as e:
    print(f'LIVENESS oakbrook: fetch error ({str(e)[:60]}) — non-blocking (email provenance lives on comallitacos twin)')
try:
    st_d, b_d = http_get(demo.split('?')[0])
    assert st_d == 200 and 'The Social' in b_d and 'West Reading' in b_d, f'demo HTTP {st_d}'
    print('LIVENESS demo: 200 branded (The Social + West Reading present)')
except SystemExit:
    raise
except Exception as e:
    sys.exit(f'ABORT: demo fetch failed ({e})')

# 5) send (body on stdin, --json envelope; message_id from the envelope JSON)
if resume_mid:
    mid = resume_mid
    print('RESUME: envelope carries ok send — NOT re-sending:', mid)
else:
    res = subprocess.run(['email', 'send', '--account', 'jarvis', '--as', 'websites',
                          '--to', TO, '--subject', SUBJ, '--json'],
                         input=BODY.encode(), capture_output=True, timeout=120)
    try:
        env = json.loads(res.stdout.decode())
    except Exception:
        open(ENVOUT, 'w').write(res.stdout.decode() + '\n---STDERR---\n' + res.stderr.decode())
        sys.exit('ABORT: unparseable send envelope — do NOT resend, read back Sent Mail first')
    json.dump({'ok': env.get('ok'), 'env': env}, open(ENVOUT, 'w'))
    ok = env.get('ok')
    mid = (env.get('data') or {}).get('message_id') or (env.get('data') or {}).get('msg_id') or env.get('message_id')
    print('SEND ok=', ok, 'msg:', mid if ok else env)
    if not ok or not mid:
        sys.exit('ABORT send — read back [Gmail]/Sent Mail before any retry')

# 6) sent read-back (raw imaplib): Message-ID equality + identity header pair.
# v6 subject carries em dash (Q-encoded on IMAP) -> search ASCII stem only, per-word proof client-side.
conf = {}
for l in open(os.path.expanduser('~/.hermes/config/jarvis-email.conf')):
    if '=' in l: k, v = l.split('=', 1); conf[k.strip()] = v.strip()
    elif ':' in l: k, v = l.split(':', 1); conf[k.strip()] = v.strip()
M = imaplib.IMAP4_SSL(conf.get('IMAP_SERVER', 'imap.gmail.com'))
M.login(conf['EMAIL'], conf['APP_PASSWORD'])
M.select('"[Gmail]/Sent Mail"')
typ, m = M.uid('search', None, 'SUBJECT', '"Your new website is live"')
ids = [i.decode() for i in m[0].split()]
hit = None
for uid in ids[-12:]:
    typ, d = M.uid('fetch', uid, '(BODY.PEEK[HEADER])')
    hdr = d[0][1].decode(errors='replace')
    if mid in hdr:
        orp = bool(re.search(r'X-Google-Original-From:[^>]*jarvis\+websites', hdr, re.I))
        rto = bool(re.search(r'Reply-To:\s*\S*jarvis\+websites', hdr, re.I))
        subj_line = ' '.join(l for l in hdr.splitlines() if l.lower().startswith('subject'))
        full = all(w.lower() in subj_line.lower() for w in ('The', 'Social')) and 'West Reading' not in subj_line and 'Oakbrook' not in subj_line
        hit = {'uid': uid, 'ogf': orp, 'reply_to': rto, 'subject_full': full}
        break
M.logout()
print('READBACK:', hit)
assert hit and hit['ogf'] and hit['reply_to'] and hit['subject_full'], 'ABORT READBACK — mail out but unproven; append registry only after proof, never re-send'

# 7) registry append AT SEND (type IN the dict), then recount-verify
TODAY = datetime.date.today().isoformat()
row = {
    'id': 'pk-' + os.urandom(5).hex(),
    'type': 'pitch', 'date': TODAY,
    'ts': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
    'slug': SLUG, 'business': 'The Social (West Reading PA)', 'city': 'West Reading', 'state': 'PA',
    'name_aliases': ['The Social', 'TheSocial', 'thesocial', 'The Social West Reading', 'socialwestreading', 'The Social bar West Reading', 'the-social-west-reading'],
    'email': TO, 'alias': TO.split('@')[0], 'card': CARD,
    'email_provenance': 'self-published on the group\u2019s OWN Facebook Page intro https://www.facebook.com/TaqueriaComalli/ (verified on-page 2026-11-25 browser pass) + printed in comallitacos.com homepage footer (live curl 200 2026-11-25, send-liveness re-checked in-script); tie: berkscountyeats.com coming-soon column + thebrewedatpodcast ep.49 + Palomagazine name Erik Arizmendi as owner of Oakbrook Brewing & Taqueria Comalli and The Social comes from that same team -> group inbox tie (Azura/Terra House + G&A/stefanolegacy class)',
    'msg_id': mid, 'preview': 'https://the-social-west-reading-demo.up.railway.app',
    'subject': SUBJ, 'subject_arm': 'v6', 'cohort': 'new_prospect',
    'shot': False, 'pixel': True, 'utm_content': TOKEN,
    'followup_due': '2026-12-04',
    'ladder': 't2 2026-12-04 / t3 2026-12-11 / t4 2026-12-18 (weekday ladder, US-holiday shift: Thanksgiving 11-26/27); teardown recheck >= 2026-12-23',
    'feed_id': 'berkscountyeats-coming-soon', 'shop_id': SLUG,
    'note': ('9-page opening-week drinks-only bar site (home/the-bar/opening/2 detail pages/contact/privacy + 404/thanks), '
             'facts berkscountyeats+press+GBP-nap only, address 643 Penn Ave West Reading PA 19611 (press loose Penn Street/19610 superseded by GBP+geocode), NO phone published, '
             'no-site evidence 11-25 dispatch: variant matrix dig+RDAP404 all noDNS; socialreading.com registered 2026-11-01 Squarespace-cluster IPs serves 114-byte JS /lander park (NOT owner site, NOT owner-proven); brand SERP press-only; GBP empty embed no pid; '
             'homonyms verified different: thesocialwc West Chester / thesocialbar814 Ridgway / Midtown Sip Savor Social 600 Penn Ave; greeting Hi Erik (press-named owner); founder bundle T1 $249+$39/mo 31d trial; '
             'projected opening Dec 2026-Jan 2027 (health inspection done, bar-service-only); v6 subject arm (deterministic coin sha256(slug)%2=0 pinned 2026-11-24); gmail inbox recipient (FB self-published); read-back proof uid='),
}
with open(REG, 'a') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
pitches = 0; mine = 0; line_no = 0
for i, l in enumerate(open(REG), 1):
    try: d = json.loads(l)
    except Exception: continue
    if d.get('type') == 'pitch':
        pitches += 1
        if d.get('slug') == SLUG: mine += 1; line_no = i  # lane.db events.line = registry PHYSICAL line
assert mine == 1, f'the-social pitch rows={mine}'
print(f'REGISTRY_OK total_pitch_rows={pitches} mine=1 line={line_no}')

# 8) lane.db events mirror row
import sqlite3
db = sqlite3.connect(LANEDB)
db.execute("""INSERT INTO events (line,type,slug,business,email,msg_id,followup_due,date_txt,ts,note)
VALUES (?,?,?,?,?,?,?,?,?,?)""",
 (line_no, 'pitch', SLUG, 'The Social (West Reading PA)', TO, mid,
  '2026-12-04', TODAY, int(time.time()),
  'pitched via websites desk; demo the-social-west-reading-demo.up.railway.app; founder bundle T1 $249+$39/mo 31d trial; v6 subject arm; group inbox tie (Oakbrook/Comalli team, press-named owner Erik Arizmendi); read-back proof uid=' + hit['uid']))
db.commit()
print('EVENT_ROW_OK', db.execute("SELECT line,type,slug,msg_id FROM events WHERE slug=?", (SLUG,)).fetchall())

# 8b) pilot-table row (11-24 execution mechanics: arm/token/age/maturity)
pt = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
db.execute("""INSERT INTO pilot (slug,arm,email,msg_id,token,pitched_ts,nudge_due,mature_on,reg_date,reg_source,age_days,age_tag,status,substantive,notes)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
 (SLUG, 'v6', TO, mid, TOKEN, pt, '2026-12-04', '2026-12-11',
  '2026-11-21', 'press-proxy age: berkscountyeats coming-soon entry Updated Nov 21 2026 (first press sighting); pre-opening brand, no LLC registration found in PA search 2026-11-25; opening projected Dec 2026-Jan 2027',
  max(0, (datetime.date.today() - datetime.date(2026, 11, 21)).days), 'brand_new', 'pending', 0,
  'arm coin sha256(slug)%2=0 -> v6 verified == mail truth; card t_1358a4a4; recipient gmail inbox self-published on group FB page; West Reading PA ET; send in-window EST morning'))
db.commit()
print('PILOT_ROW_OK', db.execute("SELECT slug,arm,token,age_tag,mature_on FROM pilot WHERE slug=?", (SLUG,)).fetchall())

# 9) close-out tz seed (idempotent; CLOSE-OUT SEEDING rule)
_ts = subprocess.run(['python3', TZG, 'set', '--slug', SLUG, '--tz', 'America/New_York', '--source', '643 Penn Ave, West Reading, PA 19611'], capture_output=True, text=True)
print('TZ_SEED:', _ts.stdout.strip() or _ts.stderr.strip())
print('ALL_DONE', mid)
