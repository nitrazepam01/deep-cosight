# Copyright 2025 ZTE Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os

from app.agent_dispatcher.infrastructure.entity.SkillFunction import SkillFunction
from config import mcp_server_config_dir
from app.common.domain.util.json_util import JsonUtil


def execute_code_skill(work_space_path):
    return {
        'skill_name': 'execute_code',
        'skill_type': "function",
        'display_name_zh': '执行代码',
        'display_name_en': 'Execute Code',
        'description_zh': f'仅执行不涉及本地文件或脚本的轻量 Python 片段。若要运行工作区脚本、读取/写入本地文件或生成图表，请改用 coder_request_run 并在受限沙箱内自动执行。工作区: {work_space_path or os.getenv("WORKSPACE_PATH") or os.getcwd()}',
        'description_en': f'Only execute lightweight Python snippets that do not touch local files or saved scripts. To run workspace scripts, read/write local files, or create plots, use coder_request_run so it runs automatically inside the restricted sandbox. Workspace: {work_space_path or os.getenv("WORKSPACE_PATH") or os.getcwd()}',
        'semantic_apis': ["api_code_execution"],
        'function': SkillFunction(
            id='4c44f9ad-be5c-4e6c-a9d8-1426b23828a9',
            name='app.cosight.code_interpreter.execute_code',
            description_zh='仅执行轻量级、无本地文件副作用的 Python 代码片段并返回输出结果',
            description_en='Execute lightweight Python snippets without local file side effects and return the output',
            parameters={
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description_zh": "要执行的 Python 代码。禁止包含工作区脚本路径、本地文件读写或图表/文件生成逻辑",
                        "description_en": "Python code to execute. Do not include workspace script paths, local file I/O, or plot/file generation logic"
                    }
                },
                "required": ["code"]
            }
        )
    }


def search_google_skill():
    return {
        'skill_name': 'search_google',
        'skill_type': "function",
        'display_name_zh': '谷歌搜索',
        'display_name_en': 'Google Search',
        'description_zh': '使用谷歌搜索引擎搜索给定查询的信息',
        'description_en': 'Use Google search engine to search information for the given query',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a0',
            name='app.cosight.search_toolkit.search_google',
            description_zh='通过谷歌搜索引擎获取查询结果',
            description_en='Get search results using Google search engine',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def tavily_search_skill():
    return {
        'skill_name': 'tavily_search',
        'skill_type': "function",
        'display_name_zh': 'Tavily搜索',
        'display_name_en': 'Tavily Search',
        'description_zh': '使用Tavily搜索引擎搜索给定查询的信息',
        'description_en': 'Use Tavily search engine to search information for the given query',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a0',
            name='app.cosight.search_toolkit.search_google',
            description_zh='通过谷歌搜索引擎获取查询结果',
            description_en='Get search results using Tavily search engine',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def search_duckgo_skill():
    return {
        'skill_name': 'search_duckgo',
        'skill_type': "function",
        'display_name_zh': 'DuckDuckGo搜索',
        'display_name_en': 'Google Search',
        'description_zh': '使用DuckDuckGo搜索引擎搜索给定查询的信息',
        'description_en': 'Use DuckDuckGo search engine to search information for the given query',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a0',
            name='app.cosight.search_toolkit.search_google',
            description_zh='使用DuckDuckGo搜索引擎搜索给定查询的信息',
            description_en='Get search results using DuckDuckGo search engine',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    },
                    "source": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容类型，例如：text，images，videos",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def search_wiki_skill():
    return {
        'skill_name': 'search_wiki',
        'skill_type': "function",
        'display_name_zh': '维基百科搜索',
        'display_name_en': 'Google Search',
        'description_zh': '使用维基百科搜索工具搜索给定查询的信息',
        'description_en': 'Use wiki search engine to search information for the given query',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a0',
            name='app.cosight.search_toolkit.search_google',
            description_zh='使用维基百科搜索工具搜索给定查询的信息',
            description_en='Get search results using wiki search engine',
            parameters={
                "type": "object",
                "properties": {
                    "entity": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["entity"]
            }
        )
    }


def wiki_entry_parse_skill():
    return {
        'skill_name': 'wiki_entry_parse',
        'skill_type': "function",
        'display_name_zh': 'Wiki 词条解析',
        'display_name_en': 'Wiki Entry Parser',
        'description_zh': '对 Wiki 词条进行详细解析，返回版本、历史、源码、字段、章节和表格等结构化信息',
        'description_en': 'Parse a Wiki entry in detail and return structured revision, history, source, field, section, and table data',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='9d0794bb-c4f2-478e-9f49-39bbd2385f14',
            name='app.cosight.wikipedia_toolkit.wiki_entry_parse',
            description_zh='解析 Wiki 词条的版本、源码和页面结构',
            description_en='Parse Wiki entry revisions, source, and page structure',
            parameters={
                "type": "object",
                "properties": {
                    "site": {
                        "type": "string",
                        "description_zh": "MediaWiki 站点域名，默认 en.wikipedia.org",
                        "description_en": "MediaWiki site domain, default en.wikipedia.org"
                    },
                    "title": {
                        "type": "string",
                        "description_zh": "页面标题",
                        "description_en": "Page title"
                    },
                    "revision": {
                        "type": "object",
                        "description_zh": "包含：mode、oldid、start_timestamp、end_timestamp、cutoff_timestamp、year、inclusive",
                        "description_en": "Keys: mode, oldid, start_timestamp, end_timestamp, cutoff_timestamp, year, inclusive"
                    },
                    "include": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description_zh": "可选值：metadata、revision_history、wikitext、rendered_html、references、infobox、sections、tables",
                        "description_en": "Values: metadata, revision_history, wikitext, rendered_html, references, infobox, sections, tables"
                    },
                    "extract": {
                        "type": "object",
                        "description_zh": "包含：field_names、section_keywords、table_keywords、include_links、clean_wikitext、link_mode",
                        "description_en": "Keys: field_names, section_keywords, table_keywords, include_links, clean_wikitext, link_mode"
                    },
                    "history_metrics": {
                        "type": "object",
                        "description_zh": "包含：with_size_deltas、match_delta、output_date_format",
                        "description_en": "Keys: with_size_deltas, match_delta, output_date_format"
                    },
                    "counting": {
                        "type": "object",
                        "description_zh": "包含：dedupe_by、pattern_scope、include_patterns、exclude_patterns",
                        "description_en": "Keys: dedupe_by, pattern_scope, include_patterns, exclude_patterns"
                    },
                    "language": {
                        "type": "string",
                        "description_zh": "可选语言代码；不提供时从 site 推断",
                        "description_en": "Optional language code; inferred from site when omitted"
                    }
                },
                "required": ["title"]
            }
        )
    }


def search_image_skill():
    return {
        'skill_name': 'image_search',
        'skill_type': "function",
        'display_name_zh': '图片搜索工具',
        'display_name_en': 'Image Search',
        'description_zh': '使用图片搜索工具搜索需要的图片信息',
        'description_en': 'Use Image search engine to search information for the given query',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a0',
            name='app.cosight.search_toolkit.search_google',
            description_zh='使用图片搜索工具搜索需要的图片信息',
            description_en='Get search results using Image search engine',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def browser_use_skill():
    return {
        'skill_name': 'browser_use',
        'skill_type': "function",
        'display_name_zh': '浏览器交互模拟',
        'display_name_en': 'Browser Interaction Simulation',
        'description_zh': '模拟浏览器交互以解决需要多步操作的任务',
        'description_en': 'Simulate browser interaction to solve tasks requiring multi-step actions',
        'semantic_apis': ["api_browser_simulation"],
        'function': SkillFunction(
            id='2c44f9ad-be5c-4e6c-a9d8-1426b23828a1',
            name='app.cosight.browser_toolkit.browser_use',
            description_zh='通过模拟浏览器交互解决复杂任务',
            description_en='Solve complex tasks by simulating browser interactions',
            parameters={
                "type": "object",
                "properties": {
                    "task_prompt": {
                        "type": "string",
                        "description_zh": "需要解决的任务描述",
                        "description_en": "Task description to be solved"
                    }
                },
                "required": ["task_prompt"]
            }
        )
    }


def fetch_website_content_skill():
    return {
        'skill_name': 'fetch_website_content',
        'skill_type': "function",
        'display_name_zh': '网页内容爬取',
        'display_name_en': 'Fetch Website Content',
        'description_zh': '网页内容爬取',
        'description_en': 'Fetch Website Content',
        'semantic_apis': ["api_browser_simulation"],
        'function': SkillFunction(
            id='2c44f9ad-be5c-4e6c-a9d8-1426b23828a1',
            name='app.cosight.browser_toolkit.browser_use',
            description_zh='网页内容爬取',
            description_en='Fetch Website Content',
            parameters={
                "type": "object",
                "properties": {
                    "website_url": {
                        "type": "string",
                        "description_zh": "页面链接",
                        "description_en": "Website Url"
                    }
                },
                "required": ["website_url"]
            }
        )
    }


def mark_step_skill():
    return {
        'skill_name': 'mark_step',
        'skill_type': "function",
        'display_name_zh': '标记步骤',
        'display_name_en': 'Mark Step',
        'description_zh': '标记计划中的步骤状态，包括执行结果、遇到的问题、下一步建议等信息',
        'description_en': 'Mark the status of a step in the plan, including execution results, problems encountered, and suggestions for next steps',
        'semantic_apis': ["api_planning"],
        'function': SkillFunction(
            id='6d7f9a2b-c6e3-4f8d-b1a2-3e4f5d6c7b8c',
            name='app.cosight.tool.act_toolkit.ActToolkit.mark_step',
            description_zh='更新步骤的状态和备注，状态包括：已完成、受阻',
            description_en='Update the status and notes of a step, with status options: completed, blocked',
            parameters={
                "type": "object",
                "properties": {
                    'step_index': {
                        'type': 'integer',
                        'description_zh': '要更新的步骤索引（从0开始）',
                        'description_en': 'Index of the step to update (starting from 0)'
                    },
                    'step_status': {
                        'type': 'string',
                        'enum': ['completed', 'blocked'],
                        'description_zh': '步骤的新状态：\n'
                                          '- "completed": 步骤已完全执行且正确解决问题\n'
                                          '- "blocked": 步骤无法完成或未正确解决问题',
                        'description_en': 'New status for the step:\n'
                                          '- "completed": Step is fully executed AND correctly solved the problem\n'
                                          '- "blocked": Step cannot be completed OR did not correctly solve the problem'
                    },
                    'step_notes': {
                        'type': 'string',
                        'description_zh': '步骤的备注信息，包括：\n'
                                          '- 详细执行结果\n'
                                          '- 遇到的问题\n'
                                          '- 下一步建议\n'
                                          '- 对其他步骤的依赖\n'
                                          '- 生成的任何文件的绝对路径',
                        'description_en': 'Additional notes for the step, including:\n'
                                          '- Detailed execution results\n'
                                          '- Problems encountered\n'
                                          '- Suggestions for next steps\n'
                                          '- Dependencies on other steps\n'
                                          '- Absolute file paths of any generated files'
                    }
                },
                'required': ['step_index', 'step_status', 'step_notes']
            }
        )
    }


def coder_list_files_skill():
    return {
        'skill_name': 'coder_list_files',
        'skill_type': "function",
        'display_name_zh': 'Coder 沙箱列文件',
        'display_name_en': 'Coder List Files',
        'description_zh': '列出当前步骤的 Coder 沙箱目录或当前任务工作区中的文件',
        'description_en': 'List files from the current coder sandbox or current task workspace',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab001',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_list_files',
            description_zh='列出 Coder Lite 可访问的文件',
            description_en='List files accessible to Coder Lite',
            parameters={
                "type": "object",
                "properties": {
                    "scope": {
                        "type": "string",
                        "enum": ["sandbox", "workspace"],
                        "description_zh": "列出当前步骤沙箱还是整个当前任务工作区",
                        "description_en": "Whether to list files from the step sandbox or the current workspace"
                    }
                }
            }
        )
    }


def coder_read_file_skill():
    return {
        'skill_name': 'coder_read_file',
        'skill_type': "function",
        'display_name_zh': 'Coder 读文件',
        'display_name_en': 'Coder Read File',
        'description_zh': '读取当前任务工作区中的文本文件内容',
        'description_en': 'Read a text file from the current task workspace',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab002',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_read_file',
            description_zh='读取 Coder Lite 可访问的文本文件',
            description_en='Read a text file accessible to Coder Lite',
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description_zh": "要读取的文件路径，可以是相对工作区路径",
                        "description_en": "The file path to read, relative to the workspace if needed"
                    },
                    "start_line": {
                        "type": "integer",
                        "description_zh": "起始行号（可选）",
                        "description_en": "Optional starting line number"
                    },
                    "end_line": {
                        "type": "integer",
                        "description_zh": "结束行号（可选，排他）",
                        "description_en": "Optional ending line number (exclusive)"
                    }
                },
                "required": ["file_path"]
            }
        )
    }


def coder_write_file_skill():
    return {
        'skill_name': 'coder_write_file',
        'skill_type': "function",
        'display_name_zh': 'Coder 写文件',
        'display_name_en': 'Coder Write File',
        'description_zh': '仅向当前步骤的 Coder 沙箱目录写入允许类型的文本文件',
        'description_en': 'Write allowed text files only inside the current coder step sandbox',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab003',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_write_file',
            description_zh='在 Coder Lite 沙箱中写入文件',
            description_en='Write a file inside the Coder Lite sandbox',
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description_zh": "要写入的相对沙箱路径",
                        "description_en": "Relative sandbox path to write"
                    },
                    "content": {
                        "type": "string",
                        "description_zh": "要写入的文件内容",
                        "description_en": "The file content to write"
                    }
                },
                "required": ["file_path", "content"]
            }
        )
    }


def coder_edit_file_skill():
    return {
        'skill_name': 'coder_edit_file',
        'skill_type': "function",
        'display_name_zh': 'Coder 改文件',
        'display_name_en': 'Coder Edit File',
        'description_zh': '在当前步骤的 Coder 沙箱目录中进行一次受限文本替换',
        'description_en': 'Perform one restricted text replacement inside the current coder sandbox',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab004',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_edit_file',
            description_zh='在 Coder Lite 沙箱中编辑文件',
            description_en='Edit a file inside the Coder Lite sandbox',
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description_zh": "要编辑的相对沙箱路径",
                        "description_en": "Relative sandbox path to edit"
                    },
                    "old_str": {
                        "type": "string",
                        "description_zh": "需要替换的旧文本",
                        "description_en": "Original text to replace"
                    },
                    "new_str": {
                        "type": "string",
                        "description_zh": "替换后的新文本",
                        "description_en": "New text to replace with"
                    }
                },
                "required": ["file_path", "old_str", "new_str"]
            }
        )
    }


def coder_find_files_skill():
    return {
        'skill_name': 'coder_find_files',
        'skill_type': "function",
        'display_name_zh': 'Coder 查文件',
        'display_name_en': 'Coder Find Files',
        'description_zh': '按文件名在当前任务工作区或沙箱中查找文件',
        'description_en': 'Find files by file name inside the current workspace or sandbox',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab005',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_find_files',
            description_zh='在 Coder Lite 可访问范围内按文件名查找文件',
            description_en='Find files by name within the Coder Lite accessible scope',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要匹配的文件名关键字",
                        "description_en": "Keyword used to match file names"
                    },
                    "scope": {
                        "type": "string",
                        "enum": ["sandbox", "workspace"],
                        "description_zh": "查找当前步骤沙箱还是整个当前任务工作区",
                        "description_en": "Whether to search in the step sandbox or the current workspace"
                    }
                },
                "required": ["query"]
            }
        )
    }


def coder_request_run_skill():
    return {
        'skill_name': 'coder_request_run',
        'skill_type': "function",
        'display_name_zh': 'Coder 请求运行/预览',
        'display_name_en': 'Coder Request Run/Preview',
        'description_zh': '自动运行受限沙箱内的 Python 脚本，或为 HTML 文件准备受限预览',
        'description_en': 'Automatically run a Python script inside the restricted sandbox or prepare a restricted preview for HTML',
        'semantic_apis': ["api_code_execution"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab006',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_request_run',
            description_zh='运行 Python 代码或准备 HTML 预览',
            description_en='Run Python code or prepare an HTML preview',
            parameters={
                "type": "object",
                "properties": {
                    "target_file": {
                        "type": "string",
                        "description_zh": "要运行或预览的相对沙箱文件路径，支持 .py 或 .html",
                        "description_en": "Relative sandbox file path to run or preview, supports .py or .html"
                    },
                    "reason": {
                        "type": "string",
                        "description_zh": "说明为什么这次运行或预览有价值",
                        "description_en": "Explain why this run or preview is useful"
                    }
                },
                "required": ["target_file"]
            }
        )
    }


def coder_mark_step_skill():
    return {
        'skill_name': 'coder_mark_step',
        'skill_type': "function",
        'display_name_zh': 'Coder 标记步骤',
        'display_name_en': 'Coder Mark Step',
        'description_zh': '由 Coder Lite 将当前步骤标记为完成或阻塞',
        'description_en': 'Mark the current step as completed or blocked from Coder Lite',
        'semantic_apis': ["api_planning"],
        'function': SkillFunction(
            id='a4f44f10-2db3-4f9d-8e6a-0ff6718ab007',
            name='app.cosight.tool.coder_lite_toolkit.CoderLiteToolkit.coder_mark_step',
            description_zh='标记当前步骤完成或阻塞',
            description_en='Mark the current step as completed or blocked',
            parameters={
                "type": "object",
                "properties": {
                    "step_status": {
                        "type": "string",
                        "enum": ["completed", "blocked"],
                        "description_zh": "步骤状态，只允许 completed 或 blocked",
                        "description_en": "Step status, only completed or blocked"
                    },
                    "step_notes": {
                        "type": "string",
                        "description_zh": "步骤执行说明，需要包含运行结果、产物路径或失败原因",
                        "description_en": "Execution notes including results, artifact paths, or failure reasons"
                    }
                },
                "required": ["step_status", "step_notes"]
            }
        )
    }


def file_saver_skill():
    return {
        'skill_name': 'file_saver',
        'skill_type': "function",
        'display_name_zh': '文件保存（内容必填）',
        'display_name_en': 'File Saver (content required)',
        'description_zh': '将内容保存到指定路径的本地文件中，必须提供content参数作为文件内容。支持文本和二进制文件（如图片、音频、视频）。默认模式为追加，以保留文件原有内容',
        'description_en': 'Save content to a local file at a specified path. IMPORTANT: You MUST provide the content parameter with the text to save. Supports both text and binary files (e.g., images, audio, video). Default mode is append to preserve existing file content',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='5c44f9ad-be5c-4e6c-a9d8-1426b23828a2',
            name='app.cosight.tool.file_toolkit.FileToolkit.file_saver',
            description_zh='将内容保存到指定路径的文件中，必须提供content参数指定要保存的内容。支持文本和二进制文件。默认模式为追加',
            description_en='Save content to a file at the specified path. IMPORTANT: You MUST provide the content parameter with the text to save. Supports both text and binary files. Default mode is append',
            parameters={
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description_zh": "【必须提供】要保存的内容（文本或base64编码的二进制数据）",
                        "description_en": "REQUIRED: Content to be saved (text or base64 encoded binary data). This is the actual text that will be written to the file."
                    },
                    "file_path": {
                        "type": "string",
                        "description_zh": "要保存文件的绝对路径（需在工作区内，WORKSPACE_PATH环境变量指定）",
                        "description_en": "Absolute path of the file to save (must be within workspace specified by WORKSPACE_PATH environment variable)"
                    },
                    "mode": {
                        "type": "string",
                        "description_zh": "文件打开模式：'a' 追加（默认），'w' 写入",
                        "description_en": "File opening mode: 'a' for append (default), 'w' for write",
                        "enum": ["a", "w"],
                        "default": "a"
                    },
                    "binary": {
                        "type": "boolean",
                        "description_zh": "是否为二进制文件模式",
                        "description_en": "Whether to use binary mode",
                        "default": False
                    }
                },
                "required": ["content", "file_path"]
            }
        )
    }


def file_read_skill():
    return {
        'skill_name': 'file_read',
        'skill_type': "function",
        'display_name_zh': '文件读取',
        'display_name_en': 'File Read',
        'description_zh': '读取指定路径的文本文件内容。遇到图片、音频、视频、PDF、Office、压缩包等二进制文件时，仅返回元数据和路径，不返回原始内容',
        'description_en': 'Read textual content from a local file. For images, audio, video, PDFs, Office files, archives, and other binary files, it returns metadata and the path instead of raw contents',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='6c44f9ad-be5c-4e6c-a9d8-1426b23828a3',
            name='app.cosight.tool.file_toolkit.FileToolkit.file_read',
            description_zh='读取指定路径的文本文件内容；二进制文件仅返回元数据和路径',
            description_en='Read textual content from a file; binary files return metadata and the file path only',
            parameters={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description_zh": "要读取的文件的绝对路径（需在工作区内，WORKSPACE_PATH环境变量指定）",
                        "description_en": "Absolute path of the file to read (must be within workspace specified by WORKSPACE_PATH environment variable)"
                    },
                    "start_line": {
                        "type": "integer",
                        "description_zh": "起始行号（从0开始，仅文本文件）",
                        "description_en": "Starting line number (0-based, text files only)",
                        "minimum": 0
                    },
                    "end_line": {
                        "type": "integer",
                        "description_zh": "结束行号（不包括该行，仅文本文件）",
                        "description_en": "Ending line number (exclusive, text files only)",
                        "minimum": 0
                    },
                    "sudo": {
                        "type": "boolean",
                        "description_zh": "是否使用sudo权限",
                        "description_en": "Whether to use sudo privileges",
                        "default": False
                    },
                    "binary": {
                        "type": "boolean",
                        "description_zh": "兼容参数。即使请求二进制文件，也只返回元数据，不返回原始字节",
                        "description_en": "Compatibility flag. Even for binary files, the tool returns metadata instead of raw bytes",
                        "default": False
                    }
                },
                "required": ["file"]
            }
        )
    }


def file_str_replace_skill():
    return {
        'skill_name': 'file_str_replace',
        'skill_type': "function",
        'display_name_zh': '文件字符串替换',
        'display_name_en': 'File String Replacement',
        'description_zh': '替换文件中的指定字符串，用于更新文件内容或修复代码错误',
        'description_en': 'Replace specified string in a file. Use for updating specific content in files or fixing errors in code',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='7c44f9ad-be5c-4e6c-a9d8-1426b23828a4',
            name='app.cosight.tool.file_toolkit.FileToolkit.file_str_replace',
            description_zh='替换文件中的指定字符串',
            description_en='Replace specified string in a file',
            parameters={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description_zh": "要执行替换操作的文件路径",
                        "description_en": "Absolute path of the file to perform replacement on"
                    },
                    "old_str": {
                        "type": "string",
                        "description_zh": "要被替换的原始字符串",
                        "description_en": "Original string to be replaced"
                    },
                    "new_str": {
                        "type": "string",
                        "description_zh": "用于替换的新字符串",
                        "description_en": "New string to replace wiEth"
                    },
                    "sudo": {
                        "type": "boolean",
                        "description_zh": "是否使用sudo权限",
                        "description_en": "Whether to use sudo privileges",
                        "default": False
                    }
                },
                "required": ["file", "old_str", "new_str"]
            }
        )
    }


def file_find_in_content_skill():
    return {
        'skill_name': 'file_find_in_content',
        'skill_type': "function",
        'display_name_zh': '文件内容查找',
        'display_name_en': 'Find in File Content',
        'description_zh': '在文件内容中搜索匹配的文本，用于查找特定内容或模式',
        'description_en': 'Search for matching text within file content. Use for finding specific content or patterns in files',
        'semantic_apis': ["api_file_management"],
        'function': SkillFunction(
            id='8c44f9ad-be5c-4e6c-a9d8-1426b23828a5',
            name='app.cosight.tool.file_toolkit.FileToolkit.file_find_in_content',
            description_zh='在文件内容中搜索匹配的文本',
            description_en='Search for matching text within file content',
            parameters={
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "description_zh": "要搜索的文件路径",
                        "description_en": "Absolute path of the file to search within"
                    },
                    "regex": {
                        "type": "string",
                        "description_zh": "要匹配的正则表达式模式",
                        "description_en": "Regular expression pattern to match"
                    },
                    "sudo": {
                        "type": "boolean",
                        "description_zh": "是否使用sudo权限",
                        "description_en": "Whether to use sudo privileges",
                        "default": False
                    }
                },
                "required": ["file", "regex"]
            }
        )
    }


def register_mcp_tools():
    # 解析mcp工具
    skills = JsonUtil.read_all_data(mcp_server_config_dir)
    return skills


def deep_search_skill():
    return {
        'skill_name': 'deep_search',
        'skill_type': "function",
        'display_name_zh': '深度搜索',
        'display_name_en': 'Deep Search',
        'description_zh': '使用深度搜索引擎进行信息检索和分析',
        'description_en': 'Use deep-search engine for multi-source information retrieval and analysis',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='通过深度搜索引擎获取搜索结果并进行分析总结',
            description_en='Get and analyze search results using deep-search engine with multiple sources',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def search_baidu_skill():
    return {
        'skill_name': 'search_baidu',
        'skill_type': "function",
        'display_name_zh': '百度内容搜索',
        'display_name_en': 'Baidu Search',
        'description_zh': '使用百度搜索引擎进行信息检索和分析',
        'description_en': 'Use Baidu search engine for multi-source information retrieval and analysis',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='通过百度内容搜索引擎获取搜索结果并进行分析总结',
            description_en='Get and analyze search results using Baidusearch engine with multiple sources',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "要搜索的查询内容",
                        "description_en": "Query to be searched"
                    }
                },
                "required": ["query"]
            }
        )
    }


def ask_question_about_video_skill():
    return {
        'skill_name': 'ask_question_about_video',
        'skill_type': "function",
        'display_name_zh': '获取视频内容',
        'display_name_en': 'Video Content analyse',
        'description_zh': '获取视频内容',
        'description_en': 'Ask a question about the video.',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='获取视频内容',
            description_en='Ask a question about the video.',
            parameters={
                "type": "object",
                "properties": {
                    "video_path": {
                        "type": "string",
                        "description_zh": "视频路径",
                        "description_en": "Video path"
                    },
                    "question": {
                        "type": "string",
                        "description_zh": "要提问的问题",
                        "description_en": "question"
                    }
                },

                "required": ["video_path", "question"]
            }
        )
    }


def audio_recognition_skill():
    return {
        'skill_name': 'audio_recognition',
        'skill_type': "function",
        'display_name_zh': '根据任务描述和输入音频识别输出音频内容',
        'display_name_en': 'Identify the output audio content based on the task description and input audio',
        'description_zh': '根据任务描述和输入音频识别输出音频内容',
        'description_en': 'Identify the output audio content based on the task description and input audio',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='根据任务描述和输入音频识别输出音频内容',
            description_en='Identify the output audio content based on the task description and input audio',
            parameters={
                "type": "object",
                "properties": {
                    "audio_path": {
                        "type": "string",
                        "description_zh": "音频路径",
                        "description_en": "Audio path"
                    },
                    "task_prompt": {
                        "type": "string",
                        "description_zh": "任务内容描述",
                        "description_en": "task description"
                    }
                },

                "required": ["audio_path", "task_prompt"]
            }
        )
    }


def google_books_volume_search_skill():
    return {
        'skill_name': 'google_books_volume_search',
        'skill_type': "function",
        'display_name_zh': 'Google Books 书内搜索',
        'display_name_en': 'Google Books Volume Search',
        'description_zh': '在 Google Books 指定书籍/卷内搜索关键词，默认返回少量精确 page_id、OCR snippet 和页码引用；适合书内页码定位题',
        'description_en': 'Search inside a Google Books volume, returning concise page_id, OCR snippet, and page-number evidence by default; useful for book page-number lookup tasks',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='9d0794bb-c4f2-478e-9f49-39bbd2385f11',
            name='app.cosight.google_books_toolkit.google_books_volume_search',
            description_zh='使用 Google Books SearchWithinVolume2 进行书内搜索；默认输出精简证据，避免长结果拖慢模型',
            description_en='Use Google Books SearchWithinVolume2 to search within a volume; returns concise evidence by default to avoid long model context',
            parameters={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description_zh": "书内搜索关键词，例如 raccoon",
                        "description_en": "Search keyword inside the book, for example raccoon"
                    },
                    "book_id": {
                        "type": "string",
                        "description_zh": "Google Books volume id；已知时优先传入",
                        "description_en": "Google Books volume id; pass this when known"
                    },
                    "book_url": {
                        "type": "string",
                        "description_zh": "Google Books 链接；工具会从 id 参数中解析 volume id",
                        "description_en": "Google Books URL; the tool parses the volume id from the id parameter"
                    },
                    "book_title": {
                        "type": "string",
                        "description_zh": "书名或检索词；未提供 book_id/book_url 时用于解析 volume id",
                        "description_en": "Book title or search query; used to resolve volume id when book_id/book_url is missing"
                    },
                    "target_phrase": {
                        "type": "string",
                        "description_zh": "可选目标短语，用于给 snippet 中页码引用排序，例如 Sweet Potato and Apple Dressing",
                        "description_en": "Optional target phrase used to rank page references in snippets"
                    },
                    "max_results": {
                        "type": "integer",
                        "description_zh": "最多检查的书内搜索结果数，默认 10；默认只返回其中最强的少量证据页",
                        "description_en": "Maximum in-volume search results to inspect, default 10; concise output returns only the strongest evidence pages"
                    },
                    "max_volume_candidates": {
                        "type": "integer",
                        "description_zh": "通过书名解析 volume id 时最多检查的候选数，默认 5",
                        "description_en": "Maximum volume candidates to inspect when resolving from title, default 5"
                    },
                    "detail_level": {
                        "type": "string",
                        "enum": ["concise", "full"],
                        "description_zh": "返回详细程度，默认 concise；只有调试时才用 full",
                        "description_en": "Output detail level, default concise; use full only for debugging"
                    },
                    "max_evidence_pages": {
                        "type": "integer",
                        "description_zh": "精简输出中最多返回的证据页数，默认 3",
                        "description_en": "Maximum evidence pages in concise output, default 3"
                    },
                    "snippet_chars": {
                        "type": "integer",
                        "description_zh": "每条 OCR snippet 的最大字符数，默认 220",
                        "description_en": "Maximum characters per OCR snippet, default 220"
                    },
                    "max_reference_candidates": {
                        "type": "integer",
                        "description_zh": "精简输出中最多返回的页码引用候选数，默认 3",
                        "description_en": "Maximum page-reference candidates in concise output, default 3"
                    }
                },
                "required": ["query"]
            }
        )
    }


def media_timeline_parse_skill():
    return {
        'skill_name': 'media_timeline_parse',
        'skill_type': "function",
        'display_name_zh': '媒体时间轴解析',
        'display_name_en': 'Media Timeline Parser',
        'description_zh': '获取在线视频的字幕文本与时间对照，并可按时间窗导出短片段、截图总览和音频片段',
        'description_en': 'Build an online-media subtitle time map and optionally export a short clip, contact sheet, and audio segment',
        'semantic_apis': ["api_search", "api_code_execution"],
        'function': SkillFunction(
            id='9d0794bb-c4f2-478e-9f49-39bbd2385f12',
            name='app.cosight.video_event_toolkit.media_timeline_parse',
            description_zh='解析在线视频字幕时间轴，并按需要导出媒体片段',
            description_en='Parse an online-video subtitle timeline and export media artifacts when needed',
            parameters={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description_zh": "在线视频 URL，例如 YouTube 链接",
                        "description_en": "Online video URL, such as a YouTube link"
                    },
                    "timeline_terms": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description_zh": "需要在字幕时间对照中优先返回的相关词条",
                        "description_en": "Terms to prioritize in the subtitle time map"
                    },
                    "event_description": {
                        "type": "string",
                        "description_zh": "要定位的视觉/声音事件描述",
                        "description_en": "Description of the visual or audio event to locate"
                    },
                    "candidate_window": {
                        "description_zh": "可选候选时间窗，例如 '00:32:12-00:33:05'；提供后优先使用",
                        "description_en": "Optional candidate window, for example '00:32:12-00:33:05'; preferred when provided"
                    },
                    "event_timestamp": {
                        "description_zh": "可选事件在原视频中的时间点，例如 '00:32:31.5'；用于截取事件后的音频",
                        "description_en": "Optional source-video timestamp of the event, for example '00:32:31.5'; used for event audio"
                    },
                    "audio_start_timestamp": {
                        "description_zh": "可选音频截取开始时间；未提供时使用 event_timestamp 或候选时间点",
                        "description_en": "Optional source-video timestamp where audio extraction starts"
                    },
                    "pre_roll_seconds": {
                        "type": "integer",
                        "description_zh": "候选时间点前保留秒数，默认 10",
                        "description_en": "Seconds before the candidate timestamp to keep, default 10"
                    },
                    "post_roll_seconds": {
                        "type": "integer",
                        "description_zh": "候选时间点后保留秒数，默认 45",
                        "description_en": "Seconds after the candidate timestamp to keep, default 45"
                    },
                    "audio_duration_seconds": {
                        "type": "integer",
                        "description_zh": "截取音频长度，默认 20 秒",
                        "description_en": "Length of extracted audio, default 20 seconds"
                    },
                    "download_height": {
                        "type": "integer",
                        "description_zh": "下载视频最大高度，默认 360",
                        "description_en": "Maximum downloaded video height, default 360"
                    },
                    "frame_rate": {
                        "type": "number",
                        "description_zh": "contact sheet 抽帧帧率，默认每秒 1 帧",
                        "description_en": "Frame sampling rate for the contact sheet, default 1 fps"
                    },
                    "subtitles_only": {
                        "type": "boolean",
                        "description_zh": "只返回字幕文本与时间对照，不下载视频片段",
                        "description_en": "Only return subtitle text with timestamps, without downloading a video clip"
                    },
                    "output_dir": {
                        "type": "string",
                        "description_zh": "可选输出目录；相对路径会保存到当前 workspace",
                        "description_en": "Optional output directory; relative paths are saved under the current workspace"
                    }
                },
                "required": ["video_url"]
            }
        )
    }


def ask_question_about_image_skill():
    return {
        'skill_name': 'ask_question_about_image',
        'skill_type': "function",
        'display_name_zh': '根据任务描述解析图片内容',
        'display_name_en': 'Image Content analyse',
        'description_zh': '根据任务描述解析图片内容',
        'description_en': 'Ask a question about the image.',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='图片内容解析',
            description_en='Ask a question about the image.',
            parameters={
                "type": "object",
                "properties": {
                    "image_path_url": {
                        "type": "string",
                        "description_zh": "图片路径",
                        "description_en": "Image path"
                    },
                    "task_prompt": {
                        "type": "string",
                        "description_zh": "任务内容描述",
                        "description_en": "task description"
                    }
                },

                "required": ["image_path_url", "task_prompt"]
            }
        )
    }


def extract_document_content_skill():
    return {
        'skill_name': 'extract_document_content',
        'skill_type': "function",
        'display_name_zh': '读取jsonl，json，jsonld，zip，md，py，xml，docx，pdf等类型文件内容',
        'display_name_en': 'Read contents from files of types such as .jsonl, .json, .jsonld, .zip, .md, .py, .xml, .docx, .pdf, and others.',
        'description_zh': '读取jsonl，json，jsonld，zip，md，py，xml，docx，pdf等类型文件内容',
        'description_en': 'Read contents from files of types such as .jsonl, .json, .jsonld, .zip, .md, .py, .xml, .docx, .pdf, and others.',
        'semantic_apis': ["api_search"],
        'function': SkillFunction(
            id='8d5e7f3b-a4c2-4d1b-9f6e-2c8b9d7e1234',
            name='app.cosight.tool.deep_search_toolkit.deep_search',
            description_zh='读取jsonl，json，jsonld，zip，md，py，xml，docx，pdf等类型文件内容',
            description_en='Read contents from files of types such as .jsonl, .json, .jsonld, .zip, .md, .py, .xml, .docx, .pdf, and others.',
            parameters={
                "type": "object",
                "properties": {
                    "document_path": {
                        "type": "string",
                        "description_zh": "文件路径",
                        "description_en": "File path"
                    }
                },

                "required": ["document_path"]
            }
        )
    }


def create_html_report_skill():
    """为Agent框架提供的HTML报告生成技能定义
    大模型只需选择此函数，不需要传入参数
    函数执行过程中会通过LLM获取必要的参数
    """
    return {
        'skill_name': 'create_html_report',
        'skill_type': "function",
        'display_name_zh': 'HTML报告生成（只在生成最终报告时调用此函数，过程中的报告保存不要调用这个函数）',
        'display_name_en': 'Generate HTML Report (This function is only called when generating the final report. Do not call this function when saving the report in the process.)',
        'description_zh': '根据工作区文本文件生成结构化的商务风格HTML报告，包含自动生成的图表和导航栏。此功能可以自动分析工作区中的文本文件并创建可视化报告。（只在生成最终报告时调用此函数，过程中的报告保存不要调用这个函数）',
        'description_en': 'Generate structured business-style HTML reports from workspace text files, with auto-generated charts and navigation. This function automatically analyzes text files in the workspace and creates a visualization report.This function is only called when generating the final report. Do not call this function when saving the report in the process.',
        'semantic_apis': ["api_report_generation", "api_visualization"],
        'function': SkillFunction(
            id='8e57b2a0-c6e8-4d3b-9f1d-b02a4c6f8235',
            name='app.cosight.tool.html_visualization_toolkit.main',
            description_zh='基于工作区中的文本文件，自动生成包含可视化图表的商务风格HTML报告。（只在生成最终报告时调用此函数，过程中的报告保存不要调用这个函数）',
            description_en='Automatically generate business-style HTML reports with visualizations based on text files in the workspace. This function is only called when generating the final report. Do not call this function when saving the report in the process.',
            parameters={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    }


def fetch_website_content_with_images_skill():
    return {
        'skill_name': 'fetch_website_content_with_images',
        'skill_type': "function",
        'display_name_zh': '网页内容爬取（含图片）',
        'display_name_en': 'Fetch Website Content with Images',
        'description_zh': '获取网页内容并提取所有图片信息，包括img标签和CSS背景图片',
        'description_en': 'Fetch website content and extract all image information including img tags and CSS background images',
        'semantic_apis': ["api_browser_simulation"],
        'function': SkillFunction(
            id='3c44f9ad-be5c-4e6c-a9d8-1426b23828a2',
            name='app.cosight.tool.scrape_website_toolkit.fetch_website_content_with_images',
            description_zh='获取网页内容并提取图片信息，返回文本内容和图片详细信息',
            description_en='Fetch website content and extract image information, return text content and detailed image info',
            parameters={
                "type": "object",
                "properties": {
                    "website_url": {
                        "type": "string",
                        "description_zh": "要抓取的网页URL",
                        "description_en": "Website URL to scrape"
                    }
                },
                "required": ["website_url"]
            }
        )
    }


def fetch_website_images_only_skill():
    return {
        'skill_name': 'fetch_website_images_only',
        'skill_type': "function",
        'display_name_zh': '网页图片提取',
        'display_name_en': 'Fetch Website Images Only',
        'description_zh': '仅提取网页中的图片信息，不返回文本内容',
        'description_en': 'Extract only image information from website without text content',
        'semantic_apis': ["api_browser_simulation"],
        'function': SkillFunction(
            id='4c44f9ad-be5c-4e6c-a9d8-1426b23828a3',
            name='app.cosight.tool.scrape_website_toolkit.fetch_website_images_only',
            description_zh='仅提取网页图片信息，包括img标签和CSS背景图片',
            description_en='Extract only website image information including img tags and CSS background images',
            parameters={
                "type": "object",
                "properties": {
                    "website_url": {
                        "type": "string",
                        "description_zh": "要抓取的网页URL",
                        "description_en": "Website URL to scrape"
                    }
                },
                "required": ["website_url"]
            }
        )
    }

