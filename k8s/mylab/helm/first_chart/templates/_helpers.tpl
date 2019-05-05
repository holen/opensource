{{- /* 定义模板, 模板名称是全局的 */}}
{{- define "mychart.labels" }}
  labels:
    generator: helm
    date: {{ now | htmlDate }}
    {{- /* 使用全局变量 */}}
    version: "{{$.Chart.Name}}-{{ $.Chart.Version }}"
{{- end }}

{{- /* mychart.app 测试缩进 */}}
{{- define "mychart.app" -}}
app_name: {{ .Chart.Name }}
app_version: "{{ .Chart.Version }}+{{ .Release.Time.Seconds }}"
{{- end }}
