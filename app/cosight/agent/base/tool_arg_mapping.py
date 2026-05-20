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
    'wiki_entry_parse': {
        'required': ['title'],
        'aliases': {
            'site': ['domain', 'wiki_site', 'mediawiki_site'],
            'title': ['page', 'page_title', 'article', 'entity'],
            'revision': ['revision_selector', 'revision_spec', 'history', 'oldid', 'revid'],
            'include': ['includes', 'evidence', 'props'],
            'extract': ['extract_options', 'fields', 'sections', 'tables'],
            'history_metrics': ['metrics', 'revision_metrics', 'audit_metrics'],
            'counting': ['count', 'counting_options', 'filters'],
            'language': ['lang'],
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
    'media_timeline_parse': {
        'required': ['video_url'],
        'aliases': {
            'video_url': ['url', 'youtube_url', 'link', 'video_link'],
            'timeline_terms': ['subtitle_terms', 'caption_terms', 'keywords', 'search_terms'],
            'event_description': ['event', 'visual_event', 'description'],
            'candidate_window': ['time_window', 'window', 'clip_window', 'section'],
            'event_timestamp': ['event_time', 'timestamp', 'visual_event_time'],
            'audio_start_timestamp': ['audio_start', 'music_start_time', 'start_audio_at'],
            'pre_roll_seconds': ['pre_roll', 'before_seconds'],
            'post_roll_seconds': ['post_roll', 'after_seconds'],
            'audio_duration_seconds': ['audio_duration', 'music_clip_seconds'],
            'download_height': ['height', 'max_height'],
            'frame_rate': ['fps', 'sample_rate'],
            'output_dir': ['output_path', 'save_dir', 'artifact_dir'],
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

