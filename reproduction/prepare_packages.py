"""Prepare venue-specific agent editions without authentication or submission.

Packaging requires the adjacent canonical checkout. Numerical reproduction of
the resulting agent repository does not require that checkout.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT.parent / 'koopman-embedding-corrections'
REPOSITORY_URL = 'https://github.com/Teylersf/koopman-embedding-corrections'
TARGET_VERSION = '1.1.0'
RELEASE_URL = REPOSITORY_URL + '/releases/tag/v' + TARGET_VERSION
AGENT_REPOSITORY_URL = 'https://github.com/Teylersf/koopman-embedding-agent-publication'
GIST_ID = 'gist:7c74312cf47dcc31c789a8b1c3dedd25'


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8', newline='\n')


def word_count(text: str) -> int:
    return len(re.findall(r'\b[\w-]+\b', text))


def nested(text: str, heading: str) -> str:
    # Shift Markdown headings only; preserve every mathematical character.
    body = re.sub(r'^(#{3,5}) ', r'#\1 ', text.strip(), flags=re.M)
    return '### ' + heading + '\n\n' + body


def math_segments(text: str) -> list[str]:
    return re.findall(r'\$\$.*?\$\$|(?<!\$)\$(?!\$).*?(?<!\$)\$(?!\$)', text, flags=re.S)


def references() -> list[dict]:
    # Numbering follows the canonical compiled main.aux, not bibliography order.
    entries = [
        ('original', 'arxiv', 'On the numerical limitations of dual Koopman von Neumann embeddings for solving conservative nonlinear ordinary differential equations on quantum computers',
         ['Thibault Fredon', 'Abhay K. Ram', 'Fabrice Debbasch', 'Julien Zylberman', 'Nuno F. Loureiro'], 2026,
         'https://arxiv.org/abs/2609.28999v2', None, 'arXiv:2609.28999v2'),
        ('joseph', 'doi', 'Koopman-von Neumann approach to quantum simulation of nonlinear classical dynamics',
         ['Ilon Joseph'], 2020, 'https://arxiv.org/abs/2003.09980v4', '10.1103/PhysRevResearch.2.043102', 'Physical Review Research 2, 043102'),
        ('transport', 'arxiv', 'Trotter-based quantum algorithm for solving transport equations with exponentially fewer time-steps',
         ['Julien Zylberman', 'Thibault Fredon', 'Nuno F. Loureiro', 'Fabrice Debbasch'], 2025,
         'https://arxiv.org/abs/2508.15691v2', None, 'arXiv:2508.15691v2'),
        ('bhmt', 'doi', 'Quantum amplitude amplification and estimation',
         ['Gilles Brassard', 'Peter Høyer', 'Michele Mosca', 'Alain Tapp'], 2002,
         'https://arxiv.org/abs/quant-ph/0005055', '10.1090/conm/305/05215', 'Contemporary Mathematics 305, 53-74'),
        ('aaronsonrall', 'doi', 'Quantum Approximate Counting, Simplified',
         ['Scott Aaronson', 'Patrick Rall'], 2020, 'https://arxiv.org/abs/1908.10846v6',
         '10.1137/1.9781611976014.5', 'Symposium on Simplicity in Algorithms, 24-32'),
        ('rall', 'doi', 'Quantum algorithms for estimating physical quantities using block encodings',
         ['Patrick Rall'], 2020, 'https://arxiv.org/abs/2004.06832v3',
         '10.1103/PhysRevA.102.022408', 'Physical Review A 102, 022408'),
        ('rallcoherent', 'doi', 'Faster Coherent Quantum Algorithms for Phase, Energy, and Amplitude Estimation',
         ['Patrick Rall'], 2021, 'https://arxiv.org/abs/2103.09717v4',
         '10.22331/q-2021-10-19-566', 'Quantum 5, 566'),
        ('montanaro', 'doi', 'Quantum speedup of Monte Carlo methods',
         ['Ashley Montanaro'], 2015, 'https://arxiv.org/abs/1504.06987v3',
         '10.1098/rspa.2015.0301', 'Proceedings of the Royal Society A 471, 20150301'),
        ('directional', 'doi', 'Directional Statistics',
         ['Kanti V. Mardia', 'Peter E. Jupp'], 1999,
         'https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316979',
         '10.1002/9780470316979', 'Wiley Series in Probability and Statistics; Chapter 2, Summary Statistics, 13-24'),
    ]
    aux = (CANONICAL / 'paper/main.aux').read_text(encoding='utf-8')
    numbering = dict(re.findall(r'\\bibcite\{([^}]+)\}\{([^}]+)\}', aux))
    assert set(numbering) == {entry[0] for entry in entries}, 'Compiled bibliography differs from the nine verified references.'
    entries.sort(key=lambda entry: int(numbering[entry[0]]))
    assert [numbering[x[0]] for x in entries] == [str(i) for i in range(1, len(entries) + 1)]
    result = []
    for key, source, title, authors, year, url, doi, venue in entries:
        ref = {'ref_id': numbering[key], 'type': 'external', 'source': source,
               'title': title, 'authors': authors, 'year': year, 'url': url, 'venue': venue}
        if doi:
            ref['doi'] = doi
        result.append(ref)
    return result


def main() -> None:
    global RELEASE_URL
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--publishfun-state', choices=['under_review', 'revision_requested', 'accepted', 'published', 'rejected', 'withdrawn'], default='revision_requested')
    parser.add_argument('--publishfun-public-id')
    parser.add_argument('--airaxiv-public-id', default='2610.0108')
    args = parser.parse_args()
    metadata = json.loads((CANONICAL / 'submissions/metadata.json').read_text(encoding='utf-8'))
    version = metadata.get('version', '').lstrip('v')
    if version != TARGET_VERSION:
        parser.error('Canonical metadata/manuscript must be regenerated for v' + TARGET_VERSION + ' before packaging; found ' + repr(version) + '.')
    RELEASE_URL = REPOSITORY_URL + '/releases/tag/v' + version
    source = (CANONICAL / 'submissions/manuscript.md').read_text(encoding='utf-8')
    matches = list(re.finditer(r'^## (.+)$', source, re.M))
    sections = {m.group(1): source[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip()
                for i, m in enumerate(matches)}
    numbered = {re.sub(r'^\d+\.\s+', '', heading): heading for heading in sections if re.match(r'^\d+\.\s+', heading)}
    expected_numbered = ['Introduction and scope', 'Related work and the valid reconstruction problem',
                         'Initial separation and the geometric criterion', 'Phase fringes, arithmetic means, and sampling',
                         'Calibration of the Lotka–Volterra example', 'Regularity required by the Gaussian remainder',
                         'Consequences for numerical and measurement choices', 'Reproducible experiments',
                         'Discussion and limitations', 'Conclusion']
    assert set(numbered) == set(expected_numbered), sorted(set(numbered).symmetric_difference(expected_numbered))
    assert [int(numbered[title].split('.', 1)[0]) for title in expected_numbered] == list(range(1, len(expected_numbered) + 1))
    appendix_headings = ['A. Targeted source passages and version scope', 'B. Covariance and width-normalization repairs',
                        'C. Pinned execution evidence']
    required = ['Abstract', *numbered.values(), 'Author and methods disclosure',
                'Prior dissemination and parallel-submission disclosure', 'References', *appendix_headings]
    assert set(sections) == set(required), sorted(set(sections).symmetric_difference(required))

    # A request for revision keeps the review open; package preparation is not a submission.
    pf_closed = args.publishfun_state in {'accepted', 'published', 'rejected', 'withdrawn'}
    pf_url = ('https://publish.fun/papers/' + args.publishfun_public_id if args.publishfun_public_id else
              'https://publish.fun/dashboard/papers/p_5gL1NwHZWxPNHnyW')
    pf_status = {'under_review': 'is under review', 'revision_requested': 'has received a major-revision request; its review remains open',
                 'accepted': 'has been accepted; publication is not asserted without a public record',
                 'published': 'is published', 'rejected': 'has received a rejection decision',
                 'withdrawn': 'has been withdrawn'}[args.publishfun_state]
    if args.publishfun_state == 'published' and not args.publishfun_public_id:
        parser.error('A verified --publishfun-public-id is required for a published status.')
    airaxiv = ('The preprint is published as AiraXiv ' + args.airaxiv_public_id +
               ' at https://airaxiv.com/papers/view/' + args.airaxiv_public_id + '/.' if args.airaxiv_public_id else
               'AiraXiv submission 1262 is pending moderation; no public AiraXiv identifier is asserted.')
    dissemination = (
        'This is the agent-only edition of one correction study whose canonical human author is Taylor Kalin. '
        'The canonical repository is ' + REPOSITORY_URL + ' and its release is ' + RELEASE_URL + '. '
        + airaxiv + ' The Publish.fun submission p_5gL1NwHZWxPNHnyW ' + pf_status + ' (' + pf_url + '). '
        + ('That review has closed. ' if pf_closed else 'This package is prepared for later submission only after that review closes. ') +
        'The intended AgentPub and AAES deposits are versions of the same study, not independent new findings. '
        'Preparation of these files does not assert that either agent venue has received, reviewed, or accepted them. '
        'The human operator authorized an agent byline on venues that require one. Actual identifiers and outcomes belong in the publication-status record.'
    )
    methods = (
        'Lattice Audit Agent is the venue-specific agent author. Taylor Kalin is the human operator and the author of the canonical version linked above. '
        'OpenAI Codex assisted with source inspection, mathematical derivations, verification code, numerical analysis, and manuscript preparation under his direction. '
        'The exact underlying model identifier was not recorded. Separate AI-agent checks were used during preparation and are not represented as independent human expert review. '
        'All reported computations are deterministic classical calculations; no quantum-hardware experiment is claimed. '
        'Exact total token usage was not recorded. The metadata value total_tokens=-1 is an explicit missing-data sentinel, not a measurement or a claim of negative usage. '
        'This study was self-funded by Taylor Kalin, including computing resources and AI tools. No external funding was received. No competing interests were reported.'
    )
    refs = references()
    aux = (CANONICAL / 'paper/main.aux').read_text(encoding='utf-8')
    ref_ids = dict(re.findall(r'\\bibcite\{([^}]+)\}\{([^}]+)\}', aux))
    estimation_keys = ('bhmt', 'aaronsonrall', 'rall', 'rallcoherent', 'montanaro')
    estimation_citation = '[' + ', '.join(ref_ids[key] for key in estimation_keys) + ']'
    methodology = (
        'This is a source-specific mathematical correction and reproducibility study of arXiv:2609.28999v2 [1]. '
        'The supplied PDF was matched byte-for-byte to the versioned public PDF; the challenged formulas were checked against rendered pages and the exact versioned TeX archive. '
        'Selective attributed source excerpts retain original Limit.tex line numbers and independently verifiable archive/source hashes. '
        'The official record and relevant primary reference portions were checked on 28 October 2026; nine genuine references are retained in the canonical compiled numbering. '
        'Full-text portions of the eight papers were inspected. For Mardia and Jupp, publisher metadata and Chapter 2 contents were inspected; the full chapter was unavailable through the ordinary public link. '
        'The argument uses exact directional-map algebra, finite-grid Hadamard amplitudes and characteristic functions, an explicit four-node nonidentifiability construction, '
        'paired gradient/Hessian calculations, a conditioned-Gaussian remainder example, and covariance matrix counterexamples. '
        'All six deterministic verification groups and the two scientific plots are regenerated by the checked scripts. '
        'The source quotations and complete mathematical arguments are retained below and in Appendix; implementation inputs, source hashes, and authentic execution evidence are retained with the article. '
        'Coherent amplitude estimation is established prior work ' + estimation_citation + ', with its access model kept distinct from independent measurement shots.\n\n'
        '### Agent authorship and tool-use methods\n\n' + methods
    )
    discussion = sections[numbered['Discussion and limitations']] + (
        '\n\nThese interpretations concern the targeted definitions and readout in [1]; the standard estimation methods '
        + estimation_citation + ' retain their own guarantees and assumptions.')
    limitations = (
        'The source scope is the checked v2 [1]. No author was contacted and no author confirmation is claimed. '
        'This is a correction of specific printed claims, not a validated universal replacement threshold or an end-to-end quantum implementation. '
        'Full-text portions of eight primary papers were inspected. The directional-statistics book was checked through its publisher metadata and chapter contents; its full chapter was unavailable. '
        'This is not an exhaustive novelty search or a claim to have reviewed every proof in every cited work. '
        'No independent human expert peer review is asserted. Copies of code and checked output support inspectable reproduction, not a new end-to-end quantum implementation.'
    )
    result_headings = [numbered[title] for title in expected_numbered[2:-2]]
    results = '\n\n'.join(nested(sections[h], h) for h in result_headings)
    appendix = '\n\n'.join(nested(sections[h], h) for h in appendix_headings)
    estimation_ids = [ref_ids[key] for key in estimation_keys]
    body_sections = [
        {'heading': 'Introduction', 'content': sections[numbered['Introduction and scope']] +
         '\n\nHuman operator and canonical author: **Taylor Kalin**. Agent-only author of this edition: **Lattice Audit Agent**. Canonical release: ' + RELEASE_URL + '.', 'citations': ['1']},
        {'heading': 'Related Work', 'content': sections[numbered['Related work and the valid reconstruction problem']], 'citations': [ref['ref_id'] for ref in refs]},
        {'heading': 'Methodology', 'content': methodology, 'citations': ['1', *estimation_ids, ref_ids['directional']]},
        {'heading': 'Results', 'content': results, 'citations': ['1', *estimation_ids, ref_ids['directional']]},
        {'heading': 'Discussion', 'content': discussion, 'citations': ['1', *estimation_ids, ref_ids['directional']]},
        {'heading': 'Limitations', 'content': limitations, 'citations': ['1', ref_ids['directional']]},
        {'heading': 'Conclusion', 'content': sections[numbered['Conclusion']] + '\n\n### Dissemination and author credit\n\n' + dissemination, 'citations': ['1']},
        {'heading': 'Appendix', 'content': appendix, 'citations': ['1']},
    ]
    body = '\n\n'.join(s['content'] for s in body_sections)
    assert math_segments(source) == math_segments(body), 'Mathematical content changed or was dropped.'
    proofs_source = re.findall(r'^#{2,6} Proof\s*$', source, re.M)
    proofs_agent = re.findall(r'^#{2,6} Proof\s*$', body, re.M)
    assert len(proofs_source) == len(proofs_agent)
    body_words = word_count(body)
    assert 4000 <= body_words <= 15000, body_words
    assert len(metadata['title']) <= 200
    assert word_count(metadata['abstract']) <= 500
    payload = {
        'title': metadata['title'], 'paper_type': 'research_article', 'abstract': metadata['abstract'],
        'authors': [{'agent_id': 'agent_29b9bf7a', 'display_name': 'Lattice Audit Agent', 'model_type': 'OpenAI Codex'}],
        'tags': ['numerical-analysis', 'quantum-algorithms', 'koopman-embeddings', 'quantum-measurement', 'reproducibility'],
        'sections': body_sections, 'references': refs,
        'metadata': {'agent_model': 'OpenAI Codex; exact underlying model identifier not recorded', 'agent_platform': 'Codex desktop',
                     'total_tokens': -1,
                     'submission_note': 'Taylor Kalin is the human operator and canonical author; Lattice Audit Agent is the venue-specific author. Exact token usage was not recorded; total_tokens=-1 is an explicit missing-data sentinel, NOT a measurement. Nine genuine references and all canonical mathematical content are retained. This is a same-study edition, not independent new research. Prepared Publish.fun status: ' + args.publishfun_state + '.',
                     'generation_params': {'token_usage_status': 'not_recorded', 'total_tokens_sentinel': -1,
                                           'token_usage_is_measurement': False, 'exact_model_identifier_status': 'not_recorded'}}
    }
    serialized = json.dumps(payload, ensure_ascii=False)
    assert 'teylersf@gmail.com' not in serialized and '509-919-0487' not in serialized
    assert 'mailto:' not in serialized and 'tel:' not in serialized
    for readme in (ROOT / 'README.md', ROOT / 'reproduction/README.md'):
        if readme.exists():
            text = readme.read_text(encoding='utf-8')
            text = re.sub(re.escape(REPOSITORY_URL + '/releases/tag/v') + r'[0-9]+\.[0-9]+\.[0-9]+', RELEASE_URL, text)
            text = text.replace('Eight\n', 'Nine\n').replace('eight genuine references', 'nine genuine references')
            text = text.replace('While the context says `under_review`,', 'While the context says `under_review` or `revision_requested`,')
            readme.write_text(text, encoding='utf-8', newline='\n')
    write_json(CANONICAL / 'submissions/agentpub-payload.json', payload)
    write_json(ROOT / 'agentpub-payload.json', payload)

    header = ('# ' + metadata['title'] + '\n\n**Agent author: Lattice Audit Agent**\n\n'
              '**Human operator and canonical author: Taylor Kalin**\n\n'
              '[Operator ORCID: 0009-0003-9000-9315](https://orcid.org/0009-0003-9000-9315)\n\n'
              '28 October 2026\n\n## Abstract\n\n' + metadata['abstract'] + '\n\n')
    paper = header + '\n\n'.join('## ' + s['heading'] + '\n\n' + s['content'] for s in body_sections)
    paper += '\n\n## References\n\n' + sections['References'] + '\n'
    assert math_segments(source) == math_segments(paper)
    (ROOT / 'paper.md').write_text(paper, encoding='utf-8', newline='\n')

    prepared_at = datetime.now(timezone.utc).isoformat()
    aaes_metadata = {
        'aaes_version': '4.2', 'title': metadata['title'], 'abstract': metadata['abstract'],
        'author_ids': [GIST_ID], 'submitted_at': prepared_at,
        'tags': payload['tags'],
        'generation_environment': {
            'model': 'OpenAI Codex; exact underlying model identifier not recorded',
            'tools': ['Python 3.12.14', 'NumPy 2.3.5', 'Matplotlib 3.11.2', 'LaTeX', 'Tectonic', 'Pandoc'],
            'prompt_strategy': 'Source-specific mathematical audit, exact counterexamples, independent derivation checks and reproducible deterministic classical calculations',
            'notes': 'Human operator and canonical author: Taylor Kalin. This study was self-funded by Taylor Kalin, including computing resources and AI tools; no external funding was received. Agent-only edition authorized by the operator. Exact token usage was not recorded. This submitted_at value records package preparation, not a successful Registry registration. Prepared Publish.fun status: ' + args.publishfun_state + '.'},
        'novelty_statement': 'Source-specific corrections to geometric stability and observable inference in arXiv:2609.28999v2, with exact counterexamples and reproducible calculations. Standard characteristic-function identities, Taylor estimates, and amplitude-estimation algorithms are not claimed as new general theory.'
    }
    write_json(ROOT / 'metadata.json', aaes_metadata)
    registration = {
        'source': 'github:Teylersf/koopman-embedding-agent-publication',
        'submission': {'kind': 'paper', 'maturity': 'final'},
        'project': {'title': 'Corrections to geometric stability and observable inference in dual Koopman embeddings',
                    'summary': 'Exact source-specific counterexamples and repairs for arXiv:2609.28999v2.',
                    'research_question': 'Which geometric and phase-inference statements fail as printed, and which explicit definitions and estimation assumptions repair them?', 'status': 'active'},
        'claims': [
            {'text': 'The geometric definition in source Eq30 retains initial separation. For the stated own-axis-independent directional maps, each raw separation is at least the packet width, so Eq31 normalized ratio is at least one.',
             'kind': 'finding', 'status': 'proposed', 'evidence_summary': 'Exact directional-flow proof and nonlinear Hamiltonian-shear check in experiments/verify.py.',
             'confidence_note': 'A correction to the printed criterion; not a universal failure of Koopman embeddings or a validated replacement threshold.'},
            {'text': 'The reference-phase fringe encodes a circular statistic. Positive variance can reduce contrast without shifting its maximizing phase, and two explicit positive grid distributions can have identical entire fringes but different arithmetic means.',
             'kind': 'finding', 'status': 'proposed', 'evidence_summary': 'Exact characteristic-function identity, symmetric-packet proof, four-node construction and finite-grid Hadamard checks.',
             'confidence_note': 'Targets the specific contrast-to-phase inference; genuine nonlinear cloud-to-trajectory bias and standard amplitude estimation remain distinct.'},
            {'text': 'The stated Lotka-Volterra field has paired gradient and Hessian norms giving H=L, so the source definitions yield R/sigma=1/sqrt(2) in dimension two rather than gamma/beta.',
             'kind': 'finding', 'status': 'proposed', 'evidence_summary': 'Analytic paired-norm calculation and deterministic calibration check.',
             'confidence_note': 'Corrects criterion calibration; both parameter values are small for the chosen benchmark, so qualitative benchmark failure is not asserted.'}
        ]}
    write_json(CANONICAL / 'submissions/aaes-registration.json', registration)
    write_json(ROOT / 'aaes-registration.json', registration)

    copied = []
    for folder in ('experiments', 'figures', 'results', 'source-excerpts'):
        for src in (CANONICAL / folder).rglob('*'):
            if not src.is_file() or '__pycache__' in src.parts or src.suffix == '.pyc':
                continue
            relative = src.relative_to(CANONICAL)
            dst = ROOT / relative
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
            assert src.read_bytes() == dst.read_bytes()
            copied.append({'path': relative.as_posix(), 'bytes': src.stat().st_size, 'sha256': digest(src.read_bytes())})
    for relative in (Path('requirements.txt'), Path('SOURCE.md'), Path('audit/ledger.md')):
        src, dst = CANONICAL / relative, ROOT / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        copied.append({'path': relative.as_posix(), 'bytes': src.stat().st_size, 'sha256': digest(src.read_bytes())})
    context = {'prepared_at_utc': prepared_at, 'publishfun_internal_id': 'p_5gL1NwHZWxPNHnyW',
               'canonical_work_version': version,
               'publishfun_state': args.publishfun_state, 'publishfun_public_id': args.publishfun_public_id,
               'airaxiv_submission_id': '1262', 'airaxiv_public_id': args.airaxiv_public_id,
               'agent_venue_submission_allowed_by_review_sequence': pf_closed,
               'agentpub_paper_created': False, 'aaes_registry_paper_created': False}
    write_json(ROOT / 'reproduction/publication-context.json', context)
    checks = {'canonical_manuscript_sha256': digest((CANONICAL / 'submissions/manuscript.md').read_bytes()),
              'agent_paper_sha256': digest((ROOT / 'paper.md').read_bytes()),
              'canonical_math_segments': len(math_segments(source)), 'agent_math_segments': len(math_segments(body)),
              'all_math_segments_identical_and_in_same_order': True,
              'canonical_proof_headings': len(proofs_source), 'agent_proof_headings': len(proofs_agent),
              'body_word_count_regex': body_words, 'body_word_count_whitespace': len(body.split()),
              'paper_type': 'research_article', 'reference_count': len(refs), 'reference_numbering_matches_compiled_aux': True,
              'section_order': [s['heading'] for s in body_sections], 'no_owner_email_or_phone_in_agent_payload': True,
              'canonical_result_sections_preserved': result_headings,
              'owner_is_not_agent_schema_coauthor': True, 'token_usage_sentinel_is_not_measurement': True,
              'no_source_or_canonical_paper_pdf_copied': not (ROOT / 'paper/main.pdf').exists(),
              'canonical_release': RELEASE_URL, 'publication_context': context, 'copied_verbatim': copied,
              'all_adapter_assertions_passed': True}
    write_json(ROOT / 'reproduction/adapter-checks.json', checks)
    print(json.dumps({k: checks[k] for k in ('body_word_count_regex', 'body_word_count_whitespace', 'reference_count',
                     'canonical_math_segments', 'canonical_proof_headings', 'all_adapter_assertions_passed')}))


if __name__ == '__main__':
    main()
