# 专属函数参数映射与必填项配置
# 仅当函数名命中此表时才进行映射；否则不做任何转换

from typing import Dict, List


# 结构：
# FUNCTION_ARG_MAPPING = {
#   'function_name_lower': {
#       'required': ['param1', 'param2'],
#       'aliases': {
#           'param1': ['alias_a', 'alias_b'],
#           'param2': ['alias_c']
#       }
#   }
# }

FUNCTION_ARG_MAPPING: Dict[str, Dict[str, Dict[str, List[str]]]] = {
    'file_saver': {
        'required': ['file_path', 'content'],
        'aliases': {
            'file_path': ['file', 'filepath', 'path', 'save_path', 'output', 'output_path', 'file_path','file_name','filename'],
            'content': ['text', 'data', 'body', 'contents', 'value','file_content'],
        }
    },
    'execute_code': {
        'required': ['code'],
        'aliases': {
            'code': ['script', 'source', 'python', 'py', 'content', 'text'],
        }
    },
    'search_baidu': {
        'required': ['query'],
        'aliases': {
            'query': ['q', 'keyword', 'keywords', 'search', 'prompt']
        }
    },
    'download_file': {
        'required': ['url'],
        'aliases': {
            'url': ['link', 'href', 'uri'],
            'filename': ['save_as', 'output', 'path', 'dest']
        }
    },
    'file_read': {
        'required': ['file'],
        'aliases': {
            'file': ['file_path', 'filepath', 'path', 'save_path', 'output', 'output_path', 'file_path','file_name','filename'],
        }
    },
    'coder_write_file': {
        'required': ['file_path', 'content'],
        'aliases': {
            'file_path': ['file', 'filepath', 'path', 'output', 'output_path', 'filename', 'file_name'],
            'content': ['text', 'data', 'body', 'contents', 'value', 'file_content'],
        }
    },
    'coder_read_file': {
        'required': ['file_path'],
        'aliases': {
            'file_path': ['file', 'filepath', 'path', 'filename', 'file_name'],
        }
    },
    'coder_edit_file': {
        'required': ['file_path', 'old_str', 'new_str'],
        'aliases': {
            'file_path': ['file', 'filepath', 'path', 'filename', 'file_name'],
            'old_str': ['old_text', 'before', 'source_text'],
            'new_str': ['new_text', 'after', 'replacement'],
        }
    },
    'coder_find_files': {
        'required': ['query'],
        'aliases': {
            'query': ['keyword', 'keywords', 'pattern', 'search'],
        }
    },
    'coder_request_run': {
        'required': ['target_file'],
        'aliases': {
            'target_file': ['file', 'file_path', 'filepath', 'path', 'script', 'entry_file'],
            'reason': ['purpose', 'why', 'run_reason'],
        }
    },
    'coder_mark_step': {
        'required': ['step_status', 'step_notes'],
        'aliases': {
            'step_status': ['status'],
            'step_notes': ['notes', 'summary', 'result'],
        }
    },
    'wiki_revision_at': {
        'required': ['title', 'cutoff_timestamp'],
        'aliases': {
            'title': ['page', 'page_title', 'article', 'entity'],
            'cutoff_timestamp': ['cutoff', 'as_of', 'as_of_timestamp', 'date', 'timestamp', 'end_time'],
            'language': ['lang'],
        }
    },
    'wiki_rail_connection_count': {
        'required': ['title', 'cutoff_timestamp'],
        'aliases': {
            'title': ['page', 'page_title', 'article', 'entity'],
            'cutoff_timestamp': ['cutoff', 'as_of', 'as_of_timestamp', 'date', 'timestamp', 'end_time'],
            'section_keyword': ['section', 'section_title', 'table', 'table_keyword'],
            'language': ['lang'],
        }
    },
    'wiki_revision_size_delta_find': {
        'required': ['title', 'target_delta'],
        'aliases': {
            'title': ['page', 'page_title', 'article', 'entity'],
            'target_delta': ['delta', 'bytes', 'byte_delta', 'n', 'N', 'street_number', 'target_bytes'],
            'year': ['calendar_year'],
            'start_timestamp': ['start', 'start_time', 'rvend'],
            'end_timestamp': ['end', 'end_time', 'rvstart'],
            'language': ['lang'],
        }
    },
    'wiki_infobox_field_lookup': {
        'required': ['title', 'field_name'],
        'aliases': {
            'title': ['page', 'page_title', 'article', 'entity'],
            'field_name': ['field', 'infobox_field', 'property', 'parameter', 'param'],
            'oldid': ['revision_id', 'revid', 'revision', 'historical_revision'],
            'language': ['lang'],
            'link_mode': ['mode', 'selection_mode'],
            'clean_templates': ['clean', 'clean_wikitext'],
        }
    },
    'taxon_binomial_verify': {
        'required': ['candidate_words'],
        'aliases': {
            'candidate_words': ['word', 'root_word', 'candidate', 'candidates', 'terms', 'synonyms'],
            'suffixes': ['suffix', 'suffix_list', 'letters', 'two_letters'],
            'expected_common_name_keyword': ['common_keyword', 'common_name_keyword', 'species_keyword'],
            'expected_family': ['family', 'taxonomic_family'],
            'wikipedia_language': ['language', 'lang'],
        }
    },
    'place_street_number_resolve': {
        'required': ['query'],
        'aliases': {
            'query': ['place', 'place_name', 'location', 'address', 'entity', 'name'],
            'region': ['city', 'area'],
            'baidu_ak': ['ak', 'api_key', 'baidu_key'],
            'max_results': ['limit', 'num_results'],
        }
    },
    'function_graph_letter_probe': {
        'required': ['equations'],
        'aliases': {
            'equations': ['equation', 'functions', 'function_list', 'formulas', 'expressions'],
            'plot_range': ['range', 'x_range', 'domain', 'window'],
            'output_image_path': ['image_path', 'output_path', 'plot_path', 'save_path'],
        }
    },
    'google_books_volume_search': {
        'required': ['query'],
        'aliases': {
            'query': ['keyword', 'term', 'search_query', 'q'],
            'book_id': ['volume_id', 'google_book_id', 'id'],
            'book_url': ['url', 'google_books_url', 'volume_url'],
            'book_title': ['title', 'book', 'volume_title'],
            'target_phrase': ['target', 'target_text', 'reference_phrase', 'phrase'],
            'max_results': ['limit', 'num_results'],
            'max_evidence_pages': ['evidence_limit', 'page_limit', 'top_pages'],
            'snippet_chars': ['snippet_length', 'max_snippet_chars', 'context_chars'],
            'max_reference_candidates': ['reference_limit', 'top_references'],
            'detail_level': ['detail', 'mode'],
        }
    },
    'document_abstract_year_count': {
        'required': ['document_path'],
        'aliases': {
            'document_path': ['file', 'file_path', 'path', 'filepath', 'document', 'document_path_or_url', 'url'],
            'publication_year': ['year', 'target_year', 'book_year'],
            'book_title': ['title', 'paper_title', 'article_title'],
            'abstract_end_markers': ['end_markers', 'markers', 'end_marker'],
            'abstract_start_markers': ['start_markers', 'start_marker'],
        }
    }
}

